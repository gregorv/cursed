
from registry import Registry

class ItemRegistry(Registry):
    @classmethod
    def create(cls, game, item):
        return cls.classes[item](game)
    
    @classmethod
    def check_validity(cls, name, bases, dict):
        return("name" in dict
               and "weight" in dict
               and "value" in dict
               and "symbol" in dict)

class Item(metaclass = ItemRegistry):
    def __init__(self, game):
        self.game = game
        self.type = self.__class__.__name__
        self.name = self.__class__.name
        self.weight = self.__class__.weight
        self.value = self.__class__.value
        self.symbol = self.__class__.symbol
        self.used_up = False
        self.container = None
        self.hotkey = None
        
    def on_ingest(self, ingester):
        pass
    
    def on_read(self, reader):
        pass


class ItemStackable:
    def __init__(self):
        self.count = 1
        
    def __getattribute__(self, name):
        if name == "weight":
            return self.count * self.__class__.weight
        else:
            return object.__getattribute__(self, name)

class ItemModifyable:
    pass

class ItemWieldable:
    def __init__(self, game):
        self.wielder = None

    def on_wield_attack(self, target):
        return False
