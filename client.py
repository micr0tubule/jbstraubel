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
    logger.start()
    postman.start()
    while True:
        await asyncio.sleep(0.2)
        for message in communicator.messages:
            try: 
                if type(message.content) == discord.Embed: 
                    await message.channel.send(embed=message.content)
                elif type(message.content) != str:
                    with BytesIO() as image_bytes:
                        message.content.save(image_bytes, 'PNG')
                        image_bytes.seek(0)
                        await message.channel.send(file=discord.File(fp=image_bytes, filename ='image.png'))
                else: 
                    await message.channel.send(message.content)
                communicator.messages.remove(message)
                del(message)
            except Exception as e: 
                print(e)
                pass 
@client.event
async def on_message(message):
    if message.author.bot: 
        return
    category = message.content.split() 
    if category[0][0] == '!':
        if not cx.work(message): 
            cx.execute(message)
    observer.check_task(message)

@client.event
async def on_member_update(before, after): 
    await logger.update_onlineticker(before.status, after.status)


@client.event 
async def on_member_join(member):
    cx.execute_greet_member(member) 
    try: 
        starting_role = discord.utils.get(client.guilds[0].roles, name='Praktikant')
        await member.edit(roles=[starting_role])
        await logger.update_memberticker(1)
    except Exception as e: 
        print(e)
        pass 

@client.event
async def on_member_leave(member): 
    await logger.update_memberticker(-1)


client.run(TOKEN)