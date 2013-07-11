
from item import comestibles
from item.itembase import ItemRegistry, Item, ItemStackable, ItemWieldable

class Container:
    def __init__(self, game):
        self.items = []
        
    def empty(self):
        i = list(map(lambda x: setattr(x, "container", None), self.items))
        self.items.remove(i)
        return i
    
    def add(self, item):
        if isinstance(item, Container):
            item = Container.empty()
        if not hasattr(item, "__next__"):
            item = [item]
        for i in item:
            i.container = self
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
        Container.__init__(self, game)
        self.map = map
        self.pos = pos
    
    def render(self):
        return "I"