from threading import Thread
import asyncio
import time 
from functools import singledispatch
from global_vars import Message
from PIL import Image
import discord 
from io import BytesIO


class Communicator: 
    def __init__(self):
        self.messages = []
        self.__init_append__()

    def __init_append__(self): 
        self.append = singledispatch(self.append)
        self.append.register(Message, self.append_message)
        self.append.register(list, self.append_list)

    def append(self, message): 
        pass 

    def append_list(self, messages): 
        for message in messages: 
            self.messages.append(message)

    def append_message(self, message): 
        self.messages.append(message)


    def start(self):
        self.send_thread = Thread(target=self.initiate_send_loop)
        self.send_thread.start()

    def initiate_send_loop(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self.send_loop())
        loop.close()

    async def send_loop(self):
        while True:
            time.sleep(1)
            for message in self.messages:
                if type(message.content) == Image: 
                    with BytesIO() as image_bytes: 
                        message.content.save(image_bytes, 'PNG')
                        image_bytes.seek(0)
                        await message.channel.send(file=discord.File(fp=image_bytes, filename='image.png'))
                else: 
                    await message.channel.send(message.content)  
                    print(type(message.content))

    def validate(self, message): 
        pass 
