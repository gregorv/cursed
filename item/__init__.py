

class Item:
    def __init__(self, game):
        self.game = game
        self.type = self.__class__.__name__
        self.name = self.__class__.name
        self.weight = self.__class__.weight
        self.value = self.__class__.value
        self.symbol = self.__class__.symbol
        self.used_up = False
        self.container = None
        
    def on_ingest(self, ingester):
        pass
    
    def on_read(self, reader):
        pass

class ItemStackable:
    def __init__(self):
        self.count = 1
        
    def __getattr__(self, name):
        if name == "weight":
            return self.count * self.__class__.weight
        else:
            return object.__getattr__(self, name)
        

class ItemWieldable:
    def on_wield_attack(self, wielder, target):
        return False
    
class Container:
    def __init__(self, game):
        self.items = []
    
    def add(self, item):
        if not hasattr(item, "__next__"):
            item = [item]
        for i in item:
            if isinstance(i, ItemStackable):
                for it2 in self.items:
                    if it2.type == i.type:
                        it2.count += i.count
                else:
                    self.items.append(i)
            else:
                self.items.append(i)
    
    def __len__(self):
        return len(self.items)
    
    def total_weight(self):
        return sum(it.weight for it in self.items)
        
class Inventory(Container):
    pass

class Pile(Container):
    def __init__(self, game, map, pos):
        self.map = map
        self.pos = pos
    
    def render(self):
        return "I"