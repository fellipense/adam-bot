# This example requires the 'message_content' intent.

import discord
import requests
import json
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()
_ollama_url = os.getenv('OLLAMA_URL')
_token = os.getenv('TOKEN')
intents = discord.Intents.all()

bot = discord.Bot(command_prefix=".", intents=intents)
turbo = False

@bot.event
async def on_ready():
    print(f"Bot online!")

@bot.command(description="Sends the bot's latency.")
async def ping(ctx): 
    await ctx.respond(f"Pong! Latency is `{bot.latency:.3f}`s")

@bot.command(description="Toggle turbo LM mode")
async def turbo(ctx):     

    global turbo
    if turbo == True:
        turbo = False
        print("TURBO OFF")
        await ctx.respond(f"Turbo mode disabled.")
    else:
        turbo = True
        print("TURBO ON")
        await ctx.respond(f"Turbo mode enabled.")

@bot.event
async def on_message(msg):
    if msg.author.bot: return
    if msg.content.startswith('/'): return


    if "adam" not in msg.content.lower(): return
    
    global turbo

    print("-------------------------------------------------------------")
    print(f"Analizando mensagem de '{msg.author.name}': '{msg.content}'")
    print()

    if turbo == True: 
        version = "7b"
        context = os.getenv('LM_INSTRUCTIONS')

        print(f"TURBO ON ({version})")
    else:
        context = os.getenv('LM_INSTRUCTIONS')
        context = context.replace("<name>", msg.author.name)
        version = "1.5b"
        print(f"TURBO OFF ({version})")

    context = context.replace("<date>", datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " (Y-m-d H:M:S)")
    context = context.replace("<name>", msg.author.name)
    context = context.replace("<where>", f"'{msg.channel.guild.name}' in '{msg.channel.name}'")

    members = []
    for member in msg.channel.members:
        members.append("'"+member.name+"'")

    context = context.replace("<users>", ", ".join(members))

    print(context)
    prompt = f"{msg.content} ({context})"

    print("-------------------------------------------------------------")

    payload = {
        "model": "deepseek-r1:" + version,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": 0.1,
            "max_tokens": -1
        }
    }

    msg.channel.typing()
    response = requests.post(_ollama_url, json=payload)

    if response.status_code == 200:
        rawRes = json.loads(response.text)['response']
        print("-------------------------------------------------------------")
        print(rawRes)
        print("-------------------------------------------------------------")
        res = rawRes.split("</think>\n\n")[1]
        
        if res.endswith('NULL'): return

        await msg.reply(res) 

    else:
        print(f"Erro na requisição: {response.status_code}")
        print(response.text)

bot.run(_token)