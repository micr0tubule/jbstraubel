from storage import storage
from global_vars import salary_of, message_of, State, Tasks, Message, ItemCats
from tasks import construct_task
from cook import Cook
from itemHandler import item_handler

class Request:
    '''
    ATTRIBUTES 
    state: current state of process of the request 
    complete: at what sate the request is finished 
    done: state == complete 
    '''
    def __init__(self, complete, message): 
        self.state = 0
        self.complete = complete
        self.done = False
        self.channel = message.channel
        self.requester = message.author
    

def change_state(function):
    def wrapper(self, message):
        state, payload = function(self, message)
        if state == State.OK:
            self.state += 1
            self.done = self.state == self.complete
        elif state == State.FAILED:
            self.done = True
        return payload
    return wrapper


class Buy(Request):
    '''
    state 0: user just made the !buy request 
    state 1: user chooses what to buy
    '''
    def __init__(self, message):
        super().__init__(2, message)
        self.cook = Cook()
    
    @change_state
    def work(self, message):
        print(self.state)
        if self.state == 0:
            foods = []
            for i in range(3): 
                food, image = self.cook.get_random_food(i)
                foods.append((i, food, image))
            self.foods = foods
            messages = []
            for food in foods:
                messages.append(
                    Message(content=food[2],
                            channel=self.channel))
            return State.OK, messages
        if self.state == 1:
            try:
                i = int(message.content[1])
                food = [food for food in self.foods if food[0] == i][0]
                name = self.cook.name(food[1], kasus='akkusativ', bestimmter_artikel=False)
                print(self.requester.id)
                storage.insert_new_item(self.requester.id, ItemCats.FOOD, food[i])
                user = storage.get_user(self.requester.id)
                price, _, _ = self.cook.info(food[1])
                if user.money.val >= price:
                    user.money(user.money.val - price)
                else: 
                    return State.OK, Message(
                        content=f'Du hast net genug Geld also verpiss dich. Geh mal lieber arbeiten du stück scheiße',
                        channel=self.channel
                    )
                return State.OK, Message(
                    content=f'du hast {name} gekauft, danke!',
                    channel=self.channel)
            except Exception as e:
                print(e) 
                pass
            try:
                command, params = message.content.split()
                if command == '!info':
                    try: i = int(params)
                    except: pass 
                    price, description, effect = self.cook.info([food for food in self.foods if food[0] == i][0][1])      
                    info = f"```Preis: {price}\nEffektivität: {effect}\n{description}\n```"
                    return State.NO_UPDATE, Message(
                        content=info,
                        channel=self.channel)
            except: 
                pass 


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
                return State.NO_UPDATE, Message(
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
        super().__init__(2, message)
        
    @change_state 
    def work(self, message=None):
        if self.state == 0:  
            items = storage.get_items_by_user_id(self.requester.id)
            names = [item_handler.name(item.category, item.subcategory) for item in items]

            answer = '' 
            for name in names: 
                answer.join(f'• {name}\n')
            return State.OK, Message(
                content=f'```{answer}```',
                channel=self.channel
            )


