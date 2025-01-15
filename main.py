import discord
import time
import random
import os
import asyncio
from openai import OpenAI
os.environ["OPENAI_API_KEY"] = os.environ['GPT']
aiClient = OpenAI()

Memory = {}

class Client(discord.Client):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')

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
        if message.content == 'Welcome Klondike!':
            if message.author.id != 309314775303585803:
                return
            
            await message.channel.send('Hello there! :3')
            async def looper():
                while True:
                    sendMessage = [{"role": "system", "content": "You are an extremely friendly bot on discord, you like to use ASCII emojis (ie. ':3' and ':D' and create your own). If anyone mentions your creator, your creator is named canoli. Your name is Klondike."}]
                    sendMessage.append({"role": "system", "content": "Say a quick random ice breaker"})
                    chat = aiClient.chat.completions.create(
                        model="gpt-4o-mini", messages = sendMessage
                    )
                    reply = chat.choices[0].message.content
                    await message.channel.send(reply)
                    await asyncio.sleep(random.randint(180,240))

            loop = asyncio.get_event_loop()
            asyncio.ensure_future(looper())
            loop.run_until_complete()
        



intents = discord.Intents.default()
intents.message_content = True

client = Client(intents=intents)
client.run(os.environ['BOT'])
