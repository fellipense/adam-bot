# This example requires the 'message_content' intent.

import discord
from dotenv import load_dotenv
import os

load_dotenv()
_token = os.getenv('TOKEN')
intents = discord.Intents.all()

bot = discord.Bot(command_prefix=".", intents=intents)

@bot.event
async def on_ready():
    print(f"Bot online!")

@bot.command(description="Sends the bot's latency.")
async def ping(ctx): 
    await ctx.respond(f"Pong! Latency is `{bot.latency:.3f}`s")

@bot.event
async def on_message(ctx):
    if ctx.author.bot: return
    if ctx.content == "oi": await ctx.reply("oi")

bot.run(_token)