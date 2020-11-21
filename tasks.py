from global_vars import State, Tasks, Message
from storage import storage

open_tasks = []

def load_tasks(client_refrence=None):
    for job in storage.jobs:
        construct_task(job.typus, job.user_id.val, client_refrence)

def construct_task(typus, user_id, client_refrence=None):
    job = storage.get_job_by_user_id(user_id)
    if typus == Tasks.MESSAGE:
        open_tasks.append(MessageTask(user_id, job.state))
    elif typus == Tasks.COFFEE:
        open_tasks.append(Coffee(user_id, job.state, client_refrence))
    elif typus == Tasks.BLOWJOB:
        open_tasks.append(BlowJob(user_id, job.state, client_refrence))


def change_state(function):
    def wrapper(self, message):
        state, payload = function(self, message)    
        if state == State.OK:
            self.state(self.state.val + 1)
            self.done = self.state.val == self.complete
        if state == State.FAILED:
            self.done = True
        return payload
    return wrapper
        

class Task():
    def __init__(self, complete, user, state):
        self.state = state
        self.user = user
        self.done = False
        self.complete = complete


class MessageTask(Task):
    def __init__(self, user, state):
        super().__init__(1, user, state)

    @change_state
    def validate_work(self, message):
        try:
            if self.state.val == 0:
                return State.OK, Message(
                    content='Du hast es geschafft eine Nachricht zu versenden! Geiles Ding!',
                    channel=message.channel
                )
            if message.author.id == self.user:
                return State.OK, True
        except Exception as e:
            print(e) 
            return State.FAILED, False    


class Coffee(Task):
    def __init__(self, user, state, client_refrence):
        super().__init__(1, user, state)
        self.client_refrence = client_refrence
    
    def find_coffee(self, string):
        string = string.lower()
        for _ in ['coffee','kaffee','espresso','macchiato',
            'latte','cappuccino', 'macha', 'Caffe', 'Cafe']:
            if _ in string: return _, True
        return None, False

    @change_state
    def validate_work(self, message):
        try:
            coffee, found = self.find_coffee(message.content)
            if found:
                user = storage.get_random_user()
                user = self.client_refrence.guilds[0].get_member(user.id.val)
                return State.OK, Message(
                    content=f'Du hast @{user.name} einen {coffee} gemacht! Formidable.',
                    channel=message.channel)
            else: 
                return State.NO_UPDATE, True
        except Exception as e:
            print(e)
            return State.FAILED, None

class BlowJob(Task):
    def __init__(self, user, state, client_refrence):
        super().__init__(1, user, state)
        self.client_refrence = client_refrence

    @change_state
    def validate_work(self, message):
        try:
            user = storage.get_random_user()
            user = self.client_refrence.guilds[0].get_member(user.id.val)
            return State.OK, Message(
                content=f'@{user.name} bedankt sich! Du erhaelst 10$',
                channel=message.channel) 
            worker = storage.get_user(self.user.id)
            worker.money(worker.money.val + 10)

        except Exception as e:
            print(e)
            return State.FAILED, None


    