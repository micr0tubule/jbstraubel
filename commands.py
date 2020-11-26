from storage import storage
from global_vars import salary_of, Message
from botrequests import Buy, Salary, Balance, GetTask, GetInventory 
from communicator import Communicator
import time

communicator = Communicator()

class CommandExecuter: 
    def __init__(self, client):
        self.client = client
        self.requests = []

    def pay_user(self, user):
        user.money += salary_of(user.role.val)
        user.last_time_paid = time.now()

    def process_message(self, message): 
        splitted_message = message.content.split()
        command = splitted_message[0][1:]
        params = message[1:] if len(splitted_message) > 1 else None
        return command, params

    def work(self, message):
        '''
        checks if message's author is in requests
        '''
        for request in self.requests:
            if request.requester == message.author and request.channel == message.channel: 
                try:
                    answer = request.work(message)
                    if answer and type(answer) == Message or type(answer) == list:
                        communicator.append(answer)                   
                    if not answer or request.done:
                        print('no answer or request done')
                        self.requests.remove(request)
                        del(request)
                    return True
                except Exception as e:
                    print(e)
                    self.requests.remove(request)
                    del(request)
        return False


    def execute(self, message):
        command, params = self.process_message(message)
        if command == 'salary':
            self.requests.append(Salary(message))
        elif command == 'buy': 
            self.requests.append(Buy(message))
        elif command == 'bal':
            self.requests.append(Balance(message))
        elif command == 'tasks':
            self.requests.append(GetTask(message, self.client))
        elif command == 'inventory': 
            self.requests.append(GetInventory(message))

        self.work(message)
