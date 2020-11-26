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
        self.append.register(Image, self.append_image)

    def append(self, message): 
        pass 
    
    def append_image(self, message): 
        self.messages.append(message)

    def append_list(self, messages): 
        for message in messages: 
            self.messages.append(message)

    def append_message(self, message): 
        self.messages.append(message)


    def start(self):
        self.send_thread = Thread(target=self.initiate_send_loop)
        self.send_thread.start()
