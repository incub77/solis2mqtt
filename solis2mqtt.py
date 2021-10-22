import minimalmodbus
import yaml
from time import sleep
from datetime import datetime
import paho.mqtt.client as mqtt_client
from mqtt_discovery import DiscoverMsg

# Load config
cfg = ...
with open('config.yaml') as yamlfile:
    cfg = yaml.load(yamlfile, yaml.Loader)

# Open RS485/modbus adapter
instrument = minimalmodbus.Instrument(cfg['device'], cfg['slave_address'])
instrument.serial.baudrate = 9600
instrument.serial.timeout = 0.35

# Load register data
solis_modbus = ...
with open('solis_modbus.yaml') as smfile:
    solis_modbus = yaml.load(smfile, yaml.Loader)

# Connect to mqtt server
mqtt = mqtt_client.Client(client_id="solis2mqtt", clean_session=True)
mqtt.username_pw_set(cfg['mqtt']['user'], cfg['mqtt']['passwd'])
if cfg['mqtt']['use_ssl']:
    mqtt.tls_set()
if cfg['mqtt']['use_ssl'] and not cfg['mqtt']['validate_cert']:
    mqtt.tls_insecure_set(True)
mqtt.connect(cfg['mqtt']['url'], cfg['mqtt']['port'])
mqtt.loop_start()

# Generate MQTT discovery topics for home-assistant
for entry in solis_modbus:
    if entry['active'] and 'homeassistant' in entry:
        mqtt.publish('homeassistant/sensor/solis2mqtt/' + entry['name'] + '/config',
                     str(DiscoverMsg(entry['description'],
                                     entry['name'],
                                     entry['unit'],
                                     entry['homeassistant']['device_class'],
                                     entry['homeassistant']['state_class'])),
                     retain=True)


# Work loop
def main():
    while True:
        print("--- " + datetime.now().isoformat() + " ---")
        no_response = False
        for entry in solis_modbus:
            if not entry['active']:
                continue

            try:
                if entry['modbus']['read_type'] == "register":
                    value = instrument.read_register(entry['modbus']['register'],
                                                     number_of_decimals=entry['modbus']['number_of_decimals'],
                                                     functioncode=entry['modbus']['function_code'],
                                                     signed=entry['modbus']['signed'])
                elif entry['modbus']['read_type'] == "long":
                    value = instrument.read_long(entry['modbus']['register'],
                                                 functioncode=entry['modbus']['function_code'],
                                                 signed=entry['modbus']['signed'])

            # NoResponseError occurs if inverter is off,
            # InvalidResponseError might happen when inverter is starting up or shutting down during a request
            except (minimalmodbus.NoResponseError, minimalmodbus.InvalidResponseError) as e:
                # in case we didn't have a exception before
                if not no_response:
                    print("Inverter not reachable")
                    no_response = True

                if 'homeassistant' in entry and entry['homeassistant']['state_class'] == "measurement":
                    value = 0
                else:
                    continue
            else:
                no_response = False
                print("%s: %s %s" % (entry['description'], value, entry['unit']))

            mqtt.publish('solis2mqtt/' + entry['name'], value, retain=True)

        # wait with next poll configured interval, or if inverter is not responding ten times the interval
        sleep(cfg['poll_interval'] if not no_response else cfg['poll_interval_if_off'])


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        mqtt.disconnect()
        print("Ctrl-C - quit")
