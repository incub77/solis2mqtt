import paho.mqtt.client as mqtt_client

class Mqtt(mqtt_client.Client):
    def __init__(self, client_id, cfg):
        super().__init__(client_id=client_id, clean_session=True)
        self.enable_logger()
        self.username_pw_set(cfg['user'], cfg['passwd'])
        if cfg['use_ssl']:
            self.tls_set()
        if cfg['use_ssl'] and not cfg['validate_cert']:
            self.tls_insecure_set(True)
        self.on_connect = self._on_connect_callback
        self.connect(cfg['url'], cfg['port'])
        self.loop_start()
        self.subscriptions = []

    def __del__(self):
        self.disconnect()

    def _on_connect_callback(self, client, userdata, flags, rc):
        if len(self.subscriptions):
            self.subscribe(self.subscriptions)

    def persistent_subscribe(self, topic):
        self.subscriptions.append((topic, 0))
        self.subscribe(topic)