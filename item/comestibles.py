
from .itembase import Item, ItemStackable

class Comestible(Item, ItemStackable):
    symbol = "%"
    
    def on_ingest(self):
        pass

class Apple(Item, ItemStackable):
    name = "Apple"
    weight = 1
    value = 5
    symbol = "%"
    heal = 5