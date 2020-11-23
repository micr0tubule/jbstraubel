from global_vars import ItemCats
from global_vars import Food
from storage import Item

class ItemHandler:
    def __init__(self):
        pass 

    def name(self, item: Item) -> str: 
        cat = item.category.val
        subcat = item.subcategory.val
        if cat == ItemCats.FOOD: 
            return { 
                Food.CORN_DOG: 'Corn Dog',
                Food.BANANA: 'Banane',
                Food.HAMBURGER: 'Hamburger',
                Food.CRAZY_HAMBURGER: 'Crazy Hamburger',
                Food.KEBAP: 'Kebap',
                Food.HOTDOG: 'Hot Dog'
            }.get(subcat)


item_handler = ItemHandler()
