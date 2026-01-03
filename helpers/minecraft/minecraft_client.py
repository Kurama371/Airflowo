from javascript import require, On, Once, console
from helpers.broker_client import broker_client
from helpers.minecraft.message_handler import handle_message

mineflayer = require("mineflayer")

class minecraft_client():
    def __init__(self, channel_name, client_name):
        self.client_name = client_name
        self.broker_instance = broker_client(channel_name, client_name)
        self.broker_instance.start()
        self.state = "BOOTING"
        
        self.mc_instance = mineflayer.createBot({
            "host": "mc.hypixel.net",
            #"port": "55429",
            "auth": "microsoft",
            "version": "1.8.9",
            "username": f"{client_name}"
        })

        client = self
        
        '''
        @On(self.mc_instance, "login")
        def on_login(bot):
            client.broker_instance.send({
                "client_name": client.client_name,
                "type": "info",
                "msg":  "Logged into mc."
            })

        @On(self.mc_instance, "spawn")
        def on_spawn(bot):
            client.broker_instance.send({
                "client_name": client.client_name,
                "type": "info",
                "msg":  "Joined the Server."
            })
        '''

        @On(self.mc_instance, "kicked")
        def on_kick(bot, reason):
            client.broker_instance.send({
                "type": "info",
                "msg": f"{reason}"
            })

        @On(self.mc_instance, "error")
        def on_error(bot, err):
            client.broker_instance.send({
                "type": "info",
                "msg": f"{err}"
            })

        @On(self.mc_instance, "messagestr")
        def on_message(bot, msg, position, json_msg, sender=None, verified=None):
            #client.broker_instance.send(f"MC_MSG:{client.client_name}:{sender} {message}")
            if position != "chat" or msg == '':
                return
            
            handle_message(msg, client)
