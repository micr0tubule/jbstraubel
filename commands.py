import discord
from storage import storage
from global_vars import salary_of, Message
from communicator import Communicator
import time
from functools import singledispatch

from request.botrequests import Casino
from request.botrequests import GreetMember
from request.botrequests import Buy
from request.botrequests import Casino
from request.botrequests import GetTask
from request.botrequests import GetInventory
from request.botrequests import Balance
from request.botrequests import Salary
from request.botrequests import AmongUsMaps

communicator = Communicator()

class CommandExecuter: 
    def __init__(self, client):
        self.client = client
        self.requests = []

        self.__init_handle_request__()

    def __init_handle_request__(self):
        self.handle_request = singledispatch(self.handle_request)
        self.handle_request.register(Casino, self.handle_casino)
        self.handle_request.register(GreetMember, self.handle_greetmember)

    def handle_request(self, request): 
        if request.requester == request.payload.author and request.channel == request.payload.channel: 
            result = request.work(request.payload)
            return result
    
    def handle_casino(self, request): 
        result = request.work(request.payload)
        return result 

    def handle_greetmember(self, request): 
        result = request.work(request.payload)
        return result

    def handle_christmas(self, request): 
        if request.payload.channel == request.channel: 
            result = request.work(request.payload)
            return result 

    def process_message(self, message): 
        splitted_message = message.content.split()
        command = splitted_message[0][1:]
        params = message.content[1:] if len(splitted_message) > 1 else None
        return command, params

    def work(self, payload=None):
        '''
        checks if message's author is in requests
        '''
        for request in self.requests:
            request.attach_payload(payload)
            triggered, result = self.handle_request(request)
            if request.done:
                self.requests.remove(request) 
            if result and not triggered: 
                communicator.append(result)
            if triggered: 
                communicator.append(result)
                return True

    def execute_greet_member(self, member):
        self.requests.append(GreetMember(member, self.client)) 
        self.work()



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
        elif command == 'blackjack': 
            self.requests.append(Casino(message, self.client))
        elif command == 'maps': 
            self.requests.append(AmongUsMaps(message))
        
        self.work(message)
