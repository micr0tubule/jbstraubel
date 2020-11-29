import discord 
from logger import Logger
import time
from threading import Thread
from commands import CommandExecuter, communicator
from observer import Observer
import asyncio
from global_vars import Message
from PIL import Image
from io import BytesIO
from news import Postman


TOKEN = 'NzcxNDk1NDY5MjEyODkzMjA1.X5s9JQ.VmWitVHPynJ_VKozTM9IDepU-94'
intents = discord.Intents.all()
client = discord.Client(intents=intents)


cx = CommandExecuter(client)
observer = Observer(client)
postman = Postman(client)
logger = Logger(client, cx)

@client.event
async def on_ready():
    await logger.start()
    postman.start()
    while True:
        await asyncio.sleep(0.5)
        for message in communicator.messages:
            if type(message.content) != str:
                with BytesIO() as image_bytes:
                    message.content.save(image_bytes, 'PNG')
                    image_bytes.seek(0)
                    await message.channel.send(file=discord.File(fp=image_bytes, filename ='image.png'))
            else: 
                await message.channel.send(message.content)
            communicator.messages.remove(message)
            del(message)

@client.event
async def on_message(message):
    if message.author.bot: 
        return
    observer.check_task(message)
    category = message.content.split() 
    if category[0][0] == '!':
        if not cx.work(message): 
            cx.execute(message)

@client.event
async def on_member_update(before, after): 
    await logger.update_onlineticker(before.status, after.status)


@client.event 
async def on_member_join(member): 
    await logger.update_memberticker(1)

@client.event
async def on_member_leave(member): 
    await logger.update_memberticker(-1)


client.run(TOKEN)