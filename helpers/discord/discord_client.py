import discord
import asyncio
from helpers.broker_client import broker_client
from helpers.discord.message_handler import *

intents = discord.Intents.default()
intents.message_content = True

class discord_client():
    def __init__(self, channel_name, client_name, token):
        self.token = token
        self.broker_instance = broker_client(channel_name, client_name)
        self.broker_instance.handler = self.handle_broker_msg
        self.broker_instance.start()
        

        self.guilds = {}
        
        self.bot = discord.Client(intents=intents)


        @self.bot.event
        async def on_ready():
            print(f"Discord bot logged in as {self.bot.user}")


        @self.bot.event
        async def on_message(msg):
            await self.handle_discord_msg(msg)
            


    async def start(self):
        await self.bot.start(self.token)
 
    #checks if a webhook from the bot exists for every channel in the config
    async def check_webhooks(self):
        for guild_name, guild_data in self.guilds.items():
            for channel_name, channel_id in guild_data["channels"].items():
                channel = self.bot.get_channel(channel_id) or await self.bot.fetch_channel(channel_id)

                webhooks = await channel.webhooks()
                webhook = next(
                    (wh for wh in webhooks if wh.user == self.bot.user),
                    None
                )

                if webhook is None:
                    webhook = await channel.create_webhook(name=f"Airflow Webhook")
                    print(f"Created webhook in {guild_name}:{channel_name}")
                    
    async def get_webhook(self, guild_name, channel_id):
        channel = self.bot.get_channel(channel_id) or await self.bot.fetch_channel(channel_id)
        webhooks = await channel.webhooks()
        webhook = next(
            (wh for wh in webhooks if wh.user == self.bot.user),
            None
        )
        if webhook is None:
            webhook = await channel.create_webhook(name=f"Airflow Webhook")
            print(f"Created webhook in {guild_name}:{channel_id}")
            return webhook
        return webhook

    def handle_broker_msg(self, msg):
        #async worker 
        result = asyncio.run_coroutine_threadsafe(
            self._handle_broker_msg(msg), 
            self.bot.loop
        )

        try:
            result.result()
        except Exception as e:
            print(f"Error sending webhook message: {e}")

        return

    async def _handle_broker_msg(self, msg):
        print(f"discord handler triggered: {msg}")

        if msg["type"] == "guild_msg":
            webhook = await self.get_webhook(msg["client_name"], self.guilds[msg["client_name"]]["channels"]["chat"])
            await self.send_webhook(webhook, msg["msg"], msg["sender"])

            webhook = await self.get_webhook(msg["client_name"], self.guilds[msg["client_name"]]["channels"]["debug"])
            await self.send_webhook(webhook, msg["msg"], msg["sender"])

        elif msg["type"] == "other_msg":
            webhook = await self.get_webhook(msg["client_name"], self.guilds[msg["client_name"]]["channels"]["debug"])
            await self.send_webhook(webhook, msg["msg"])

    
    async def send_webhook(self, webhook, msg, sender='Hypixel'):
        if sender == "Hypixel":
            avatar = 'https://i.imgur.com/rCXph15.png'
        elif sender == "Airflow":
            avatar = 'https://i.imgur.com/UUcZHJo.png'
        else:
            avatar = f"https://www.mc-heads.net/avatar/{sender}"
        await webhook.send(
            msg,
            username=sender,
            avatar_url=avatar
        )

    async def handle_discord_msg(self, msg):
        if msg.author.bot:
            return

        for guild_name, guild_data in self.guilds.items():
            channels = guild_data.get("channels", {})

            for channel_name, channel_id in channels.items():
                if msg.channel.id == channel_id:
                    print(f"Message sent in {guild_name}:{channel_name}")

                    if has_blocked_parts(msg.content) or has_blocked_parts(msg.author.name):
                        webhook = await self.get_webhook(guild_name, self.guilds[guild_name]["channels"]["debug"])
                        await self.send_webhook(webhook, f"Message blocked: {msg.content}", "Airflow")
                        return
                    
                    if channel_name == "chat":
                        self.broker_instance.send({
                            "type": "discord_msg",
                            "msg": f"{msg.content}",
                            "sender": f"{msg.author.name}",
                            "guild": f"{guild_name}",
                            "staff": False
                        })
                    elif channel_name == "debug":
                        self.broker_instance.send({
                            "type": "discord_msg",
                            "msg": f"{msg.content}",
                            "sender": f"{msg.author.name}",
                            "guild": f"{guild_name}",
                            "staff": True
                        })
                    return
                


    