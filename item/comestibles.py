
from .itembase import Item, ItemStackable

class Comestible(Item, ItemStackable):
    symbol = "%"
    
    def __init__(self, game):
        Item.__init__(self, game)
        ItemStackable.__init__(self)

    def on_ingest(self):
        pass

class Apple(Comestible):
    name = "Apple"
    weight = 1
    value = 5
    symbol = "%"
    heal = 5