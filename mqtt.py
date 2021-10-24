import paho.mqtt.client as mqtt_client

class Mqtt(mqtt_client.Client):
    def __init__(self, client_id, cfg):
        super().__init__(client_id=client_id, clean_session=True)
        self.username_pw_set(cfg['user'], cfg['passwd'])
        if cfg['use_ssl']:
            self.tls_set()
        if cfg['use_ssl'] and not cfg['validate_cert']:
            self.tls_insecure_set(True)
        self.connect(cfg['url'], cfg['port'])
        self.loop_start()
        
    def __del__(self):
        if self.is_connected():
            self.disconnect()