import minimalmodbus
import yaml
from time import sleep
from datetime import datetime
from mqtt_discovery import DiscoverMsg
from inverter import Inverter
from mqtt import Mqtt
from config import Config
import daemon


class Solis2Mqtt:
    def __init__(self):
        self.cfg = Config('config.yaml')
        self.register_cfg = ...
        self.load_register_cfg()
        self.inverter = Inverter(self.cfg['device'], self.cfg['slave_address'])
        self.mqtt = Mqtt(self.cfg['inverter']['name'], self.cfg['mqtt'])

    def load_register_cfg(self, register_data_file='solis_modbus.yaml'):
        with open(register_data_file) as smfile:
            self.register_cfg = yaml.load(smfile, yaml.Loader)

    def generate_HA_discovery_topics(self):
        for entry in self.register_cfg:
            if entry['active'] and 'homeassistant' in entry:
                self.mqtt.publish(f"homeassistant/sensor/{self.cfg['inverter']['name']}/{entry['name']}/config",
                             str(DiscoverMsg(entry['description'],
                                             entry['name'],
                                             entry['unit'],
                                             entry['homeassistant']['device_class'],
                                             entry['homeassistant']['state_class'],
                                             self.cfg['inverter']['name'],
                                             self.cfg['inverter']['model'],
                                             self.cfg['inverter']['manufacturer'])),
                             retain=True)

    def read_composed_date(self, register, functioncode):
        year = self.inverter.read_register(register[0], functioncode=functioncode)
        month = self.inverter.read_register(register[1], functioncode=functioncode)
        day = self.inverter.read_register(register[2], functioncode=functioncode)
        hour = self.inverter.read_register(register[3], functioncode=functioncode)
        minute = self.inverter.read_register(register[4], functioncode=functioncode)
        second = self.inverter.read_register(register[5], functioncode=functioncode)
        return f"20{year:02d}-{month:02d}-{day:02d}T{hour:02d}:{minute:02d}:{second:02d}"

    def main(self):
        self.generate_HA_discovery_topics()
        while True:
            print("--- " + datetime.now().isoformat() + " ---")
            no_response = False
            for entry in self.register_cfg:
                if not entry['active']:
                    continue

                try:
                    if entry['modbus']['read_type'] == "register":
                        value = self.inverter.read_register(entry['modbus']['register'],
                                                         number_of_decimals=entry['modbus']['number_of_decimals'],
                                                         functioncode=entry['modbus']['function_code'],
                                                         signed=entry['modbus']['signed'])
                    elif entry['modbus']['read_type'] == "long":
                        value = self.inverter.read_long(entry['modbus']['register'],
                                                     functioncode=entry['modbus']['function_code'],
                                                     signed=entry['modbus']['signed'])
                    elif entry['modbus']['read_type'] == "composed_datetime":
                        value = self.read_composed_date(entry['modbus']['register'],
                                                        functioncode=entry['modbus']['function_code'])
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

                self.mqtt.publish(f"{self.cfg['inverter']['name']}/{entry['name']}", value, retain=True)

            # wait with next poll configured interval, or if inverter is not responding ten times the interval
            sleep(self.cfg['poll_interval'] if not no_response else self.cfg['poll_interval_if_off'])


if __name__ == '__main__':
    with daemon.DaemonContext(stdout=open("out.log", "w+"), stderr=open("err.out", "w+"), working_directory='./'):
        Solis2Mqtt().main()