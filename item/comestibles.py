
from .itembase import Item, ItemStackable, ItemComestible

class Apple(Item, ItemStackable, ItemComestible):
    name = "Apple"
    weight = 1
    value = 5
    symbol = "%"
    heal = 5