import discord
from ..request import Request, change_state
from storage import storage
from itemHandler import item_handler
from global_vars import State, Message
from inventory import Inventory

class GetInventory(Request): 
    def __init__(self, message): 
        super().__init__(1, message)


    def parse_message(self, message): 
        splitted = message.content.split()
        if len(splitted) > 1: 
            return splitted
        else: 
            return splitted[0], False

    @change_state 
    def work(self, message=None):
        command, params = self.parse_message(message)
        if self.state == 0: 
            items = storage.get_items_by_user_id(self.requester.id)
            item_objs = [item_handler.construct_item(item) for item in items]
            embed = discord.Embed(title='Inventory', color=0xffc800)
            inventory = Inventory(item_objs)
            
            if params: 
                for field in inventory.fields:
                    print(params) 
                    print(field.name.lower())
                    if params.lower() in field.name.lower():
                        print('yeess') 
                        field_string = ''
                        for item in field.get_set(): 
                            field_string += f'{item.name} ×{inventory.count(item)} \n'
                        embed.add_field(name=field.name, value=field_string)
                        break
            else: 
                for field in inventory.fields:
                    field_string = ''
                    for i, item in enumerate(field.get_set()): 
                        if i > 3: 
                            field_string += '...'
                            break
                        field_string += f'{item.name} ×{inventory.count(item)} \n'
                    embed.add_field(name=field.name, value=field_string)

            return State.OK, Message(
                content=embed,
                channel=self.channel)
