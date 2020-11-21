from storage import storage
from commands import communicator
from tasks import open_tasks, load_tasks
from global_vars import Message

class Observer:
    def __init__(self, client):
        load_tasks(client)
        
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

        
            # except Exception as e:
                #     print('in observer, check_task  ')
                #     print(e)
