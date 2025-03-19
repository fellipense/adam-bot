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

@bot.event
async def on_ready():
    print(f"Bot online!")

@bot.command(description="Sends the bot's latency.")
async def ping(ctx): 
    await ctx.respond(f"Pong! Latency is `{bot.latency:.3f}`s")

@bot.event
async def on_message(msg):
    if msg.author.bot: return

    print("-------------------------------------------------------------")
    print(f"Analizando mensagem de '{msg.author.name}': '{msg.content}'")
    print()

    context = os.getenv('LM_INSTRUCTIONS')
    context = context.replace("<date>", datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " (Y-m-d H:M:S)")
    context = context.replace("<name>", msg.author.name)
    context = context.replace("<where>", f"'{msg.channel.guild.name}' in '{msg.channel.name}'")

    members = []
    for member in msg.channel.members:
        members.append("'"+member.name+"'")

    context = context.replace("<users>", ", ".join(members))

    print(context)
    print("-------------------------------------------------------------")

    payload = {
        "model": "deepseek-r1:7b",  # Nome do modelo que você baixou
        "prompt": f"Context: [{context}] Message: [{msg.content}]",
        "stream": False,
        "options": {
            "temperature": 0.1,  # Controla a criatividade do modelo
            "max_tokens": -1  # Número máximo de tokens (-1 significa sem limite)
        }
    }

    # Fazendo a requisição POST
    response = requests.post(_ollama_url, json=payload)

    # Verificando se a requisição foi bem-sucedida
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
        print(response.text)  # Exibe a mensagem de erro, se houver

bot.run(_token)