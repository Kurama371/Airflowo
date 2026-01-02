from javascript import require, On, Once, console
from helpers.broker_client import broker_client


mineflayer = require("mineflayer")

class minecraft_client():
    def __init__(self, channel_name, client_name):
        self.client_name = client_name
        self.broker_instance = broker_client(channel_name, client_name)
        self.broker_instance.start()
        
        self.mc_instance = mineflayer.createBot({
            "host": "mc.hypixel.net",
            #"port": "55429",
            "auth": "microsoft",
            "version": "1.8.9"
        })

        client = self
        

        @On(self.mc_instance, "login")
        def on_login(self):
            client.broker_instance.send({
                "client_name": client.client_name,
                "type": "info",
                "msg":  "Logged into mc."
            })

        @On(self.mc_instance, "spawn")
        def on_spawn(self):
            client.broker_instance.send({
                "client_name": client.client_name,
                "type": "info",
                "msg":  "Joined the Server."
            })

        @On(self.mc_instance, "messagestr")
        def on_message(self, msg, position, json_msg, sender=None, verified=None):
            #client.broker_instance.send(f"MC_MSG:{client.client_name}:{sender} {message}")
            if position != "chat":
                return

            client.broker_instance.send({
                "type": "mc_msg",
                "msg":  f"{msg}",
                "position": f"{position}",
            })

        @On(self.mc_instance, "kicked")
        def on_kick(self, reason):
            client.broker_instance.send({
                "type": "info",
                "msg": f"{reason}"
            })

        @On(self.mc_instance, "error")
        def on_error(self, err):
            client.broker_instance.send({
                "type": "info",
                "msg": f"{err}"
            })