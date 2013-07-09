
class NPCRegistry(type):
    npc_classes = []
    def __new__(mcs, name, bases, dict):
        cls = type.__new__(mcs, name, bases, dict)
        if("min_dungeon_level" in dict
           and "symbol" in dict
           and "name" in dict):
            mcs.npc_classes.append(cls)
        return cls
    
    @classmethod
    def upto_dungeonlevel(cls, dg_lvl):
        return list(filter(lambda npc: npc.min_dungeon_level <= dg_lvl, cls.npc_classes))
    
class ItemRegistry(type):
    item_classes = []
    def __new__(mcs, name, bases, dict):
        cls = type.__new__(mcs, name, bases, dict)
        if("min_dungeon_level" in dict
           and "weight" in dict
           and "name" in dict):
            mcs.item_classes.append(cls)
        return cls

    @classmethod
    def upto_dungeonlevel(cls, dg_lvl):
        return list(filter(lambda item: item.min_dungeon_level <= dg_lvl, cls.item_classes))
    
    @classmethod
    def names_upto_dungeonlevel(cls, dg_lvl):
        return [c.name for c in cls.upto_dungeonlevel(dg_lvl)]
    
    @classmethod
    def by_name(cls, name):
        for item in cls.item_classes:
            if item.name == name:
                return item
        else:
            raise ValueError("Item not found")