import json
from copy import deepcopy

# Generate MQTT discovery message for home-assistant
# for more info: https://www.home-assistant.io/docs/mqtt/discovery/

class DiscoverMsgSensor():
    DISCOVERY_MSG = {"name": "",
                     "state_topic": "",
                     "unique_id": "",
                     "device_class": "",
                     "state_class": "",
                     "unit_of_measurement": "",
                     "device": {"name": "",
                                "model": "",
                                "manufacturer": "",
                                "identifiers": "solis2mqtt",
                                "sw_version": "solis2mqtt "
                                }
                     }

    def __init__(self, name, id, unit, device_class, state_class,
                 device_name, device_model, device_manufacturer, version):
        self.discover_msg = deepcopy(DiscoverMsgSensor.DISCOVERY_MSG)
        self.discover_msg["name"] = name
        self.discover_msg["state_topic"] = device_name + "/" + id
        self.discover_msg["unique_id"] =  device_name + "/" +id
        self.discover_msg["device_class"] = device_class
        self.discover_msg["state_class"] = state_class
        self.discover_msg["unit_of_measurement"] = unit
        self.discover_msg["device"]["name"] = device_name
        self.discover_msg["device"]["model"] = device_model
        self.discover_msg["device"]["manufacturer"] = device_manufacturer
        self.discover_msg["device"]["sw_version"] += str(version)

    def __str__(self):
        return json.dumps(self.discover_msg)

class DiscoverMsgNumber():
    DISCOVERY_MSG = {"name": "",
                     "state_topic": "",
                     "command_topic": "",
                     "unique_id": "",
                     "min": "",
                     "max": "",
                     "step": "",
                     "device": {"name": "",
                                "model": "",
                                "manufacturer": "",
                                "identifiers": "solis2mqtt",
                                "sw_version": "solis2mqtt"
                                }
                     }

    def __init__(self, name, id, min, max, step, device_name, device_model, device_manufacturer, version):
        self.discover_msg = deepcopy(DiscoverMsgNumber.DISCOVERY_MSG)
        self.discover_msg["name"] = name
        self.discover_msg["state_topic"] = device_name + "/" + id
        self.discover_msg["command_topic"] = device_name + "/" + id + "/set"
        self.discover_msg["unique_id"] =  device_name + "/" +id
        self.discover_msg["min"] = min
        self.discover_msg["max"] = max
        self.discover_msg["step"] = step
        self.discover_msg["device"]["name"] = device_name
        self.discover_msg["device"]["model"] = device_model
        self.discover_msg["device"]["manufacturer"] = device_manufacturer
        self.discover_msg["device"]["sw_version"] += str(version)

    def __str__(self):
        return json.dumps(self.discover_msg)

class DiscoverMsgSwitch():
    DISCOVERY_MSG = {"name": "",
                     "state_topic": "",
                     "command_topic": "",
                     "unique_id": "",
                     "payload_on": "",
                     "payload_off": "",
                     "device": {"name": "",
                                "model": "",
                                "manufacturer": "",
                                "identifiers": "solis2mqtt",
                                "sw_version": "solis2mqtt"
                                }
                     }

    def __init__(self, name, id, payload_on, payload_off, device_name, device_model, device_manufacturer, version):
        self.discover_msg = deepcopy(DiscoverMsgSwitch.DISCOVERY_MSG)
        self.discover_msg["name"] = name
        self.discover_msg["state_topic"] = device_name + "/" + id
        self.discover_msg["command_topic"] = device_name + "/" + id + "/set"
        self.discover_msg["unique_id"] =  device_name + "/" +id
        self.discover_msg["payload_on"] = payload_on
        self.discover_msg["payload_off"] = payload_off
        self.discover_msg["device"]["name"] = device_name
        self.discover_msg["device"]["model"] = device_model
        self.discover_msg["device"]["manufacturer"] = device_manufacturer
        self.discover_msg["device"]["sw_version"] += str(version)

    def __str__(self):
        return json.dumps(self.discover_msg)

