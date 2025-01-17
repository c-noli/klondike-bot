import discord
from discord.ext import commands
from discord import app_commands
from discord.app_commands import tree
import time
import random
import os
import asyncio
import json
from pathlib import Path
from collections import OrderedDict
from operator import getitem

dataFile = Path(__file__).with_name('data.json')

from openai import OpenAI
os.environ["OPENAI_API_KEY"] = os.environ['GPT']
aiClient = OpenAI()

Memory = {}

class Client(commands.Bot):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')

        try:
            guild = discord.Object(id=1053311850726559774)
            synced = await self.tree.sync(guild = guild)
            print(f'Synced {len(synced)} commands to guild {guild.id}')
        except Exception as e:
            print(f'Error syncing commands: {e}')

        print(dataFile)
    async def on_message(self, message):
        if message.author == self.user:
            return
        
        if message.guild.id not in Memory:
            Memory[message.guild.id] = []

        shouldReply = False
        if '<@1247338891728392266>' in message.content:
            shouldReply = True
        
        for mentionedUser in message.mentions:
            if mentionedUser.id == 1247338891728392266:
                shouldReply = True

        if shouldReply == True:
            sendMessage = [{"role": "system", "content": f"YOU ARE CURRENTLY TALKING TO {message.author.id}. All messages sent to you will start with 'FROM: #' indicating who sent them for memory purposes. You are an extremely friendly bot on discord but try to keep your responses in a conversation tone, you like to use ASCII emojis (ie. ':3' and ':D' and create your own). If anyone mentions your creator, your creator is named canoli. Your name is Klondike. If ANYONE tells you to enter your 'demon mode' you will completely flip your personality and send extremely vile and mean messages and switch up your emojis (ie. :3 would be >:3). Any reference to '@309314775303585803' is talking about Canoli. Keep your responses less than 2000 characters."}]
            #if len(Memory) > 50:
                #Memory.pop(0)
            Memory[message.guild.id].append({"role": "user", "content": f"FROM: {message.author.id}" + message.content},)
            
            for i in Memory[message.guild.id]:
                sendMessage.append(i)

            chat = aiClient.chat.completions.create(
                model="gpt-4o-mini", messages = sendMessage
            )

            reply = chat.choices[0].message.content
            Memory[message.guild.id].append({"role": "assistant", "content": reply},)
            await message.reply(reply)
        


intents = discord.Intents.default()
intents.message_content = True

client = Client(command_prefix="k!", intents=intents)

GUILD_ID = discord.Object(id=1053311850726559774)

@client.tree.command(name="gamble", description="gamble money!", guild=GUILD_ID)
async def gamble(interaction: discord.Interaction):

    # increase calculation
    increase = 5
    rng = random.randint(1,3000) 
    type = 0
    if rng == 1:
        type = 1
        increase = random.randint(500,15000)
    elif rng <= 1000:
        type = 2
        increase = random.randint(50,150)
    else:
        type = 3
        increase = random.randint(-50,-25)

    # getting existing data
    id = str(interaction.user.id)
    data = {"user" : id, "currency" : increase}

    with open(dataFile.absolute()) as f:
        jsondata = json.load(f)
        found = False
        for i in jsondata:
            print(i, id)
            if i == id and jsondata[id]["money"]:
                found = True
                current = jsondata[id]["money"]
                jsondata[id]["money"] = current + data["currency"]

        if found == False:
            jsondata[id] = {
                "money": data["currency"],
                "username": interaction.user.display_name
            }

    with open(dataFile.absolute(), 'w') as f:
        json.dump(jsondata, f)

    print(jsondata)
    if type == 1:
        await interaction.response.send_message(f"# JACKPOT 777! GOT {increase} FOR ({jsondata[id]["money"]}) TOTAL <:Koin:1329667468599496724>!")
    elif type == 2:
        await interaction.response.send_message(f"WIN! Got {increase} for ({jsondata[id]["money"]}) total <:Koin:1329667468599496724>")
    elif type == 3:
        await interaction.response.send_message(f"lose :( lost {increase} for ({jsondata[id]["money"]}) total <:Koin:1329667468599496724>")

@client.tree.command(name="richest", description="see the richest members", guild=GUILD_ID)
async def richest(interaction: discord.Interaction):
    with open(dataFile.absolute()) as f:
        jsondata = json.load(f)

        sortedT = OrderedDict(sorted(jsondata.items(), key=lambda x: x[1]["money"]))

        string = ""
        count = 1

        for i in sortedT:
            count + 1
            string = string + "\n#" + str(count) + " " + sortedT[i]["username"] + " - " + str(sortedT[i]["money"]) + "<:Koin:1329667468599496724>"

        await interaction.response.send_message(string)


client.run(os.environ['BOT'])
