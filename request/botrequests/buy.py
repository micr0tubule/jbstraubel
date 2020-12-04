from ..request import Request, change_state
from global_vars import ItemCats, Message, State
from itemHandler import item_handler
from Item import Food, Possession
from storage import storage

class Buy(Request):
    '''
    state 0: user just made the !buy request 
    state 1: user chooses what to buy
    '''
    def __init__(self, message):
        super().__init__(2, message)
        self.category = None
        self.possession_pointer = 0
    
    def for_sale(self, item): 
        if item.user_id == 'for sale': 
            return True
        else: 
            False

    def parse_message(self, message):
        try: 
            command, params = message.content.split()
            return command, params
        except Exception as e: 
            print(e)
            return False

    def handle_request(self, category): 
    

        if self.category == ItemCats.FOOD or category == 'food':
            self.category = ItemCats.FOOD 
            return self.food()
        elif self.category == ItemCats.POSSESSION or category == 'possession': 
            self.category = ItemCats.POSSESSION
            return self.possession()
        else: 
            return False
    
    def food(self):
        self.items = item_handler.get_random(3, Food)
        messages = []
        for i, item in enumerate(self.items): 
            messages.append(Message(
                content=item.get_image(num=i),
                channel=self.channel))
        return messages
    
    def possession(self): 
        self.items = storage.get(ItemCats.POSSESSION) 
        self.items = [item_handler.construct_item(item, user_id=item.user_id.val) for item in self.items]
        self.items = list(filter(self.for_sale, self.items))
        messages = []
        for i, item in enumerate(self.items[self.possession_pointer:]): 
            self.possession_pointer += 1 
            messages.append(Message(
                content=item.get_image(num=i),
                channel=self.channel
            ))
            if self.possession_pointer % 3 == 0: 
                return messages
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
            print(result)
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
            if message.content == '!next':
                result = self.handle_request(self.category) 
                return State.NO_UPDATE, Message(
                    content=result,
                    channel=self.channel
                )
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