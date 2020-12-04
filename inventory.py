from global_vars import ItemCats
from Item import Food, Possession
from copy import copy, deepcopy

class Field: 
    def __init__(self, name):
        self.items = []
        self.name = name 
    
    def get_set(self): 
        itemset = []
        for item in self.items: 
            inset = False
            for item_ in itemset: 
                if item_.name == item.name:
                    inset = True
            if not inset: 
                itemset.append(item)
        return itemset

    def append(self, item): 
        print('appending to ', self.name)
        self.items.append(item)

class Inventory: 
    def __init__(self, items): 
        self.items = items 
        self.food = Field('🍔 Food')
        self.possession = Field('🏠 Possessions')
        for item in self.items:
            cat = type(item).__bases__[0]
            if cat == Food:
                self.food.append(item)
            elif cat == Possession: 
                self.possession.append(item)    
        self.fields = [self.food, self.possession]

    def count(self, item):      
        field = {
            Food: self.food,
            Possession: self.possession
        }.get(type(item).__bases__[0])
        return len([item_ for item_ in self.items if item.get_name()==item_.get_name()])