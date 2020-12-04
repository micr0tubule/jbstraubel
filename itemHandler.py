from image_processing.standard import scale, number
from global_vars import ItemCats
from global_vars import Food as FoodCats, Possession as PossessionCats
from Item import Food, Possession
from Item import Banana, Corndog, Hotdog, Kebap, Hamburger, CrazyHamburger, RoastedAlmonds, ChildrenTea, BakedApple, CandiedApple
from Item import House
from storage import Item
import random 

class ItemHandler:
    def __init__(self):
        pass 
    
    def get_random(self, amount, category=None):
        items = []
        for i in range(amount):  
            if category == Food:
                items.append(random.choice([Banana, Corndog, Hotdog, Kebap, Hamburger, CrazyHamburger, RoastedAlmonds, ChildrenTea, BakedApple, CandiedApple])())
        return items


    def construct_item(self, item):
        category = item.category.val 
        subcategory = item.subcategory.val
        return {
            ItemCats.FOOD: {
                FoodCats.BANANA: Banana(),
                FoodCats.CORN_DOG: Corndog(),
                FoodCats.CRAZY_HAMBURGER: CrazyHamburger(),
                FoodCats.HAMBURGER: Hamburger(),
                FoodCats.KEBAP: Kebap(),
                FoodCats.ROASTED_ALMONDS: RoastedAlmonds(),
                FoodCats.HOTDOG: Hotdog(),
                FoodCats.CHILDREN_TEA: ChildrenTea(),
                FoodCats.BAKED_APPLE: BakedApple(),
                FoodCats.CANDIED_APPLE: CandiedApple() 
            }.get(subcategory),
            ItemCats.POSSESSION: {
                PossessionCats.HOUSE: House(item)
            }.get(subcategory)
        }.get(category)


item_handler = ItemHandler()
