# This example requires the 'message_content' intent.

import discord
from dotenv import load_dotenv
import os

load_dotenv()

_token = os.getenv('TOKEN')

class MyClient(discord.Client):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')

    async def on_message(self, message):
        print(f'Message from {message.author}: {message.content}')

intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)
client.run(_token)
