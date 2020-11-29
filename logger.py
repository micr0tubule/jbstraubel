from discord import Guild
import discord
import time 
from storage import storage
from threading import Thread 
import time 
import datetime
from global_vars import LOG_TIME, AVAILABLE_TASKS_NUM, role, Tasks
import random 
import asyncio

class Logger:
    def __init__(self, client, cx):
        self.client_reference = client
        self.cx = cx
        

    def log_users(self): 
        storage.update_users([member.id for member in self.client_reference.guilds[0].members])
        for user in storage.users:       
            dcuser = self.client_reference.guilds[0].get_member(user.id.val)
            if dcuser:    
                user.role(max([role(r.name) for r in dcuser.roles]))
    

    def renew_tasks(self):
        now = datetime.datetime.now()
        if not hasattr(self, 'last_renewed_tasks'):
            self.last_renewed_tasks = now - datetime.timedelta(minutes=5)
        if abs(self.last_renewed_tasks.minute - now.minute) >= 5:
            storage.available_tasks = [Tasks.get_random(Tasks) for i in range(AVAILABLE_TASKS_NUM)]
            self.last_renewed_tasks = now


    def log_loop(self):         
        while True:
            self.log_users()
            self.renew_tasks()
            time.sleep(LOG_TIME)


    def get_online_members(self):
        online = 0 
        for member in self.client_reference.guilds[0].members: 
            if str(member.status) != 'offline': 
                online += 1 
        return online


    async def start(self): 
        self.online_channel = discord.utils.get(self.client_reference.guilds[0].channels, name='online')
        self.member_channel = discord.utils.get(self.client_reference.guilds[0].channels, name='mitarbeiter')

        self.online_members = self.get_online_members()
        await self.set_onlineticker()

        self.members = len(self.client_reference.guilds[0].members)
        await self.set_memberticker()

        self.log_thread = Thread(target=self.log_loop)
        self.log_thread.start()
        print('logger is logging..')


    async def set_onlineticker(self): 
        string = f'🟢 | online: {self.online_members}'
        await self.online_channel.edit(name=string)

    async def update_onlineticker(self, os, ns):
        if str(os) == 'offline': 
            self.online_members += 1  
        if str(ns) == 'offline': 
            self.online_members -= 1
        string = f'🟢 | online: {self.online_members}'
        await self.online_channel.edit(name=string)

    async def set_memberticker(self):
        print('setting memberticker: ', self.members)
        string = f'👥 | mitarbeiter: {self.members}' 
        await self.member_channel.edit(name=string)

    async def update_memberticker(self, state):
        '''
        state can be either:  
        - 1 for member joined 
        - -1 for member left 
        '''

        self.members += state 
        string = f'👥 | mitarbeiter: {self.members}'
        await self.member_channel.edit(name=string)



