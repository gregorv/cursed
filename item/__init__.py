
from item import comestibles
from item.itembase import ItemRegistry, Item, ItemStackable, ItemWieldable

class Container:
    def __init__(self, game):
        self.items = []

    def get_hotkeys(self):
        return [it.hotkey for it in self.items]

    def get_unused_hotkey(self):
        hotkeys = self.get_hotkeys()
        ranges = [
                  (ord("a"), ord("z")+1),
                  (ord("A"), ord("Z")+1)
                  ]
        for r in ranges:
            for i in range(*r):
                ch = chr(i)
                if ch not in hotkeys:
                    return ch
        return None

    def empty(self):
        i = list(map(lambda x: setattr(x, "container", None), self.items))
        self.items.remove(i)
        return i

    def add(self, item):
        if isinstance(item, Container):
            item = Container.empty()
        try:
            it = iter(item)
        except TypeError:
            item = [item]
        for i in item:
            if i.container:
                i.container.items.remove(i)
            i.container = self
            i.hotkey = self.get_unused_hotkey()
            if isinstance(i, ItemStackable):
                for it2 in self.items:
                    if it2.type == i.type:
                        it2.count += i.count
                        break
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