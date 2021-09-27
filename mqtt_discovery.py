import json
from copy import deepcopy

# Generate MQTT discovery message for home-assistant
# for more info: https://www.home-assistant.io/docs/mqtt/discovery/

class DiscoverMsg():
    DISCOVERY_MSG = {"name": "",
                     "state_topic": "solis2mqtt/",
                     "unique_id": "",
                     "device_class": "",
                     "state_class": "",
                     "unit_of_measurement": "",
                     "device": {"name": "solis2mqtt",
                                "model": "solis2mqtt",
                                "manufacturer": "incub",
                                "identifiers": "solis2mqtt"
                                }
                     }

    def __init__(self, name, id, unit, device_class, state_class="measurement"):
        self.discover_msg = deepcopy(DiscoverMsg.DISCOVERY_MSG)
        self.discover_msg["name"] = name
        self.discover_msg["state_topic"] = DiscoverMsg.DISCOVERY_MSG["state_topic"] + id
        self.discover_msg["unique_id"] = "solis2mqtt/"+id
        self.discover_msg["device_class"] = device_class
        self.discover_msg["state_class"] = state_class
        self.discover_msg["unit_of_measurement"] = unit

    def __str__(self):
        return json.dumps(self.discover_msg)
