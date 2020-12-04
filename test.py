from storage import storage
from global_vars import salary_of, message_of, State, Tasks, Message, ItemCats
from tasks import construct_task
from cook import Cook
from itemHandler import item_handler
import discord 
from Item import Food

class Request:
    '''
    ATTRIBUTES 
    state: current state of process of the request 
    complete: at what sate the request is finished 
    done: state == complete 
    '''
    def __init__(self, complete, message=None): 
        self.state = 0
        self.complete = complete
        self.done = False
        if message: 
            self.channel = message.channel
            self.requester = message.author

    def attach_payload(self, payload):
        self.payload = payload 
        

def change_state(function):
    def wrapper(self, message):
        state, payload = function(self, message)
        if state == State.SKIP: 
            return False, payload
        if state == State.OK:
            self.state += 1
            print('added 1 to state of ', type(self), self.state)
            self.done = self.state == self.complete
        elif state == State.FAILED:
            self.done = True
        return True, payload
    return wrapper


class Buy(Request):
    '''
    state 0: user just made the !buy request 
    state 1: user chooses what to buy
    '''
    def __init__(self, message):
        super().__init__(2, message)
        self.cook = Cook()
        self.category = None
    
    def parse_message(self, message):
        try: 
            command, params = message.content.split()
            return command, params
        except Exception as e: 
            print(e)
            return False

    def handle_request(self, category): 
        if category == 'food':
            self.category = ItemCats.FOOD 
            return self.food()
        else: 
            return False
    
    def food(self):
        self.items = item_handler.get_random(3, Food)
        messages = []
        for i, item in enumerate(self.items): 
            print(i)
            messages.append(Message(
                content=item.get_image(num=i),
                channel=self.channel))
        return messages

    def validate_transaction(self, user, item):
        return user.money.val >= item.price 


    @change_state
    def work(self, message):
        if self.state == 0:

            parsed = self.parse_message(message)
            if not parsed: 
                return State.FAILED, None
            _, category = parsed
            result = self.handle_request(category)
            if result:
                return State.OK, result
            else: 
                return State.FAILED, None

        elif self.state == 1:
            parsed = self.parse_message(message)
            if parsed: 
                command, params = parsed
                if command == '!info': 
                    try: 
                        i = int(params)
                        return State.NO_UPDATE, Message(
                            content=self.items[i].get_info(),
                            channel=self.channel)
                    except Exception as e: 
                        print(e)
                        return State.SKIP, None
            try: 
                i = int(message.content[1])
                item = self.items[i]
            except Exception as e: 
                print(e)
                return State.SKIP, None 
            user = storage.get_user(self.requester.id)
            if self.validate_transaction(user, item): 
                storage.insert_new_item(self.requester.id, self.category, item.objId)
                user.money(user.money.val - item.price)
                return State.OK, Message(
                    content=f'du hast {item.get_name()} gekauft, danke!',
                    channel=self.channel)
            else:
                return State.OK, Message(
                    content=f'Du hast net genug Geld also verpiss dich. Geh mal lieber arbeiten du stück scheiße',
                    channel=self.channel)

class Salary(Request): 
    '''
    state 0: user just made the !salary restquest
    '''
    def __init__(self, message):
        super().__init__(1, message) 

    @change_state
    def work(self, message=None):
        for u in storage.users: 
            if u.id.val == self.requester.id:
                return True, Message(
                    content=message_of('salary', self.state, salary_of(u.role.val)), 
                    channel=self.channel)
    

class Balance(Request):
    def __init__(self, message):
        super().__init__(1, message)

    @change_state
    def work(self, message=None):
        for u in storage.users:
            if u.id.val == self.requester.id:
                return True, Message(
                    content=message_of('balance', self.state, u.money.val),
                    channel=self.channel)


class GetTask(Request):
    def __init__(self, message, client):
        super().__init__(2, message)
        self.client = client

    @change_state
    def work(self, message=None):
        if self.state == 0:
            job = storage.get_job_by_user_id(self.requester.id)
            if job:
                self.done = True
                return State.SKIP, Message(
                    content = message_of('gettask', 'A', Tasks.get_name(Tasks,job.typus)),
                    channel = self.channel)

            var = 'Aktuell gibt es folgende Dinge zu erledigen: \n' \
                + ''.join([f'[{i}] {Tasks.get_name(Tasks, task)} \n' \
                for i, task in enumerate(storage.available_tasks)])

            return State.OK, Message(
                content=message_of('gettask', self.state, var),
                channel = self.channel)

        if self.state == 1:
            try:
                task_num = int(message.content[1])
                task = storage.available_tasks[task_num]
                storage.available_tasks.remove(task)
                storage.insert_new_job(self.requester.id, task, 0)
                construct_task(task, self.requester.id, self.client)
                return State.OK, Message(
                    content=message_of('gettask', self.state, Tasks.get_name(Tasks, task)),
                    channel = self.channel)
            except Exception as e:
                print(e)
                return State.FAILED, None


class GetInventory(Request): 
    def __init__(self, message): 
        super().__init__(1, message)
        
    @change_state 
    def work(self, message=None):
        if self.state == 0:  
            print('hallo')
            items = storage.get_items_by_user_id(self.requester.id)
            item_objs = [item_handler.construct_item(item) for item in items]
            names = [item.get_name() for item in item_objs]
            # names = [item_handler.name(item) for item in items]
            answer = ''.join([f'• {name}\n' for name in names])
            return State.OK, Message(
                content=f'```{answer}```',
                channel=self.channel)

class GreetMember(Request): 
    def __init__(self, member, client): 
        super().__init__(1)
        self.member = member
        self.channel = discord.utils.get(client.guilds[0].channels, id=782953651978633246)

    @change_state
    def work(self, message=None): 
        print('nice')
        return State.OK, Message(
            content=f'```@{self.member.name} Willkommen bei Mesla Totors!```',
            channel=self.channel)
