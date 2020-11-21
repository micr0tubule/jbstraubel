from discord import Guild
import time 
from storage import storage
from threading import Thread 
import time 
import datetime
from global_vars import LOG_TIME, AVAILABLE_TASKS_NUM, role, Tasks
import random 


class Logger:
    def __init__(self, client, cx):
        self.client = client
        self.cx = cx

    def log_users(self): 
        storage.update_users([member.id for member in self.client.guilds[0].members])
        for user in storage.users:       
            dcuser = self.client.guilds[0].get_member(user.id.val)
            if dcuser:    
                user.role(max([role(r.name) for r in dcuser.roles]))
    
    def check_if_work_finished(self):
        pass 


    def start(self): 
        self.log_thread = Thread(target=self.log_loop)
        self.log_thread.start()

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
            self.check_if_work_finished()
            time.sleep(LOG_TIME)

