import threading
import redis
import json

class broker_client:
    def __init__(self, channel_name, client_name):
        self.channel_name = channel_name
        self.client_name = client_name
        self.r = redis.Redis(host="localhost", port=6379, decode_responses=True)
        self.broker = self.r.pubsub()

    def send(self, msg):
        msg["client_name"] = self.client_name
        self.r.publish(self.channel_name, json.dumps(msg))

    def listen(self):
        self.broker.subscribe(self.channel_name)
        for message in self.broker.listen():
            if message["type"] != "message":
                continue

            try:
                msg = json.loads(message["data"])
            except json.JSONDecodeError:
                print("Invalid JSON:", message["data"])
                continue

            print(msg)

            #print(f"Sender: {msg[0]} - Message: {msg}")

    def start(self):
        listener = threading.Thread(target=self.listen, daemon=True)
        listener.start()