from threading import Thread

import paho.mqtt.client as mqtt
from paho.mqtt.client import Client


# -------------------------------------------- CLASSE CLIENT MQTT ----------------------------------------------------------
class MQTTClient(object):
    def __init__(self, username, password, topics, my_queues):
        self.username = username
        self.password = password
        self.queues = my_queues
        self.topics = topics
        self.client = Client(client_id="telegram_client")
        thread0 = Thread(target=self.run, args=())
        thread0.start()

    def run(self):
        self.client.tls_set(tls_version=mqtt.ssl.PROTOCOL_TLS)
        self.client.username_pw_set(username=self.username, password=self.password)

        self.client.connect(host="2de97254567d4bff9dd9184c3910ace3.s1.eu.hivemq.cloud", port=8883)
        self.client.on_connect = self.mqtt_connect
        for topic in self.topics:
            self.client.subscribe(topic)
        
        self.client.on_message = self.mqtt_onmessage

        self.client.loop_forever()

    def mqtt_connect(self, broker, userdata, flags, rc):
        print(f"MQTT: connesso al broker, result code: {str(rc)}")

    def mqtt_onmessage(self, client, userdata, msg):
        payload = msg.payload.decode("utf-8")
        queue = self.queues[msg.topic]
        queue.put(payload)
        print("Messaggio ricevuto dal topic: " + msg.topic)

    def publish(self, topic, payload):
        self.client.publish(topic=topic, payload=payload)