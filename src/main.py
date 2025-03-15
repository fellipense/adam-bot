# This example requires the 'message_content' intent.

import discord
from dotenv import load_dotenv
import os

load_dotenv()
_token = os.getenv('TOKEN')

bot = discord.Bot()

@bot.command(description="Sends the bot's latency.")
async def ping(ctx): 
    await ctx.respond(f"Pong! Latency is {bot.latency}")


bot.run(_token)