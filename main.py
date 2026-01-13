import asyncio
import json
import os
from dotenv import load_dotenv
from helpers.minecraft.minecraft_client import minecraft_client
from helpers.discord.discord_client import discord_client
from helpers.logger import setupLogging

#logging setup
setupLogging()

#load config
with open("config.json", "r", encoding="utf-8") as f:
    config = json.load(f)

#discord bot
load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
dc_client = discord_client("penguinscanfly", "discord", DISCORD_TOKEN)


for guild, channels in config["guilds"].items():
    #setup discord channels
    dc_client.guilds[guild] = channels

    #mc clients
    #mc_client_main = minecraft_client("penguinscanfly", guild)


#mc_client_main = minecraft_client("penguinscanfly", "main")

async def main():
    asyncio.create_task(dc_client.start())

    while True:
        await asyncio.sleep(1)

asyncio.run(main())




