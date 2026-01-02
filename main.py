import redis
import threading
import time

r = redis.Redis(host="localhost", port=1337, decode_responses=True)
broker = r.pubsub()

def listen():
    broker.subscribe("penguinscanfly")
    print("[A] Listening")

    for message in broker.listen():
        if message["type"] == "message":
            print("[A] Received: ", message["data"])

listener = threading.Tread(target=listen, daemon=True)
listener.start()

while True:
    msg = input("Message to send: ")
    r.publish("chat", msg)