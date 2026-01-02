from helpers.broker_client import broker_client


broker_client_2 = broker_client("penguinscanfly","Minecraft")
broker_client_2.start()

while True:
    msg = input("Message to send: ")
    broker_client_2.send(msg)