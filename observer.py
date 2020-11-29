from storage import storage
from commands import communicator
from tasks import open_tasks, load_tasks
from global_vars import salary_threshold
from global_vars import salary_of
from global_vars import Message
import discord

class Observer:
    def __init__(self, client):
        load_tasks(client)
        self.client_reference = client
        
    def add_workdone(self, user_id):
        user = storage.get_user(user_id)
        user.work_done(user.work_done.val + 1)

    def check_task(self, message):
        for task in open_tasks:    
            if task.user == message.author.id:
                job = storage.get_job_by_user_id(task.user)
                result = task.validate_work(message=message)
                if result and type(result) == Message:
                    communicator.append(result)
                if not result or task.done:
                    storage.del_job(job)
                    open_tasks.remove(task)
                    if task.done:
                        self.add_workdone(job.user_id.val)
        
        for user in storage.users: 
            try:
                if user.work_done.val % salary_threshold == 0 and user.work_done.val != 0: 
                    user.money(user.money.val + salary_of(user.role.val))
                    dcuser = self.client_reference.guilds[0].get_member(user.id.val)
                    channel = discord.utils.get(self.client_reference.guilds[0].channels, name='bot')
                    communicator.append(Message(
                        content=f"```hey @{dcuser.name}!\ndu warst fleißig, du erhälst {salary_of(user.role.val)}$! ```", 
                        channel=channel))
                    user.work_done(0)
            except Exception as e:
                pass 



