
import random
import stringfragments as frgmnt
from registry import ItemRegistry

class Item:
    def __init__(self, game):
        self.game = game
        self.name = self.__class__.name
        self.weight = self.__class__.weight
        self.symbol = self.__class__.symbol

class ItemStackable(Item):
    def __init__(self, game):
        Item.__init__(self, game)
        self.count = 1
    
#class Sword(Item):
    #symbol = "T"
    #def on_throw(self, thrower, target):
        #Item.on_throw(thrower, target)
        #target.damage(self.weight)
        
    #def on_quaff(self, quaffer):
        #quaffer.kill("You feel excrutiating pain while forcing the blade of the {0} down your throat.".format(self.name))

#class Scroll(Item):
    #symbol = "s"
    #def on_throw(self, thrower, target):
        #Item.on_throw(thrower, target)
        #target.damage(1)
        
    #def on_read(self, reader):
        #Item.on_read(thrower, target)
        
    #def on_quaff(self, quaffer):
        #self.game.logger("The {0} tastes like {1}".format(self.name,
                                                          #random.choice(frgmnt.flavour)))
        #quaffer.heal(1)
        #quaffer.spirit_bonus += 0.25
        #quaffer.mana = quaffer.max_mana

#class Potion(Item):
    #symbol = "P"
    #def effect(self, target):
        #return False
    
    #def on_throw(self, thrower, target):
        #Item.on_throw(thrower, target)
        #self.effect(target)
        #self.destroyed = True
        
    #def on_quaff(self, quaffer):
        #self.effect(quaffer)
        
    #def on_wield_attack(self, wielder, target):
        #self.destroyed = True
        #return self.effect(target)

#class Food(Item):
    #symbol = "%"
    
    #def on_quaff(self, quaffer):
        #quaffer.heal(10)
        
        
#class HealthPoiton(Potion):
    #name = "Health Potion"
    #weight = 1
    #min_dungeon_level = 1
    #def effect(self, target):
        #target.heal(50)

#class LargeHealthPoiton(Potion):
    #name = "Large Health Potion"
    #weight = 4
    #min_dungeon_level = 7
    #def effect(self, target):
        #target.heal(200)

#class PoisonPoiton(Potion):
    #name = "Poison"
    #weight = 1
    #min_dungeon_level = 5
    #def effect(self, target):
        #target.damage(100)

#class ManaPoiton(Potion):
    #name = "Mana Poiton"
    #weight = 1
    #min_dungeon_level = 1
    #def effect(self, target):
        #target.mana = min(target.mana + 100, target.max_mana)
        
#class RustySword(Sword):
    #name = "Rusty Sword"
    #weight = 20
    #min_dungeon_level = 1
    #def on_wield_attack(self, wielder, target):
        #wielder.strength_bonus += 0.01
        #return target.damage(max(1, wielder.strength/2))

#class OrcishDagger(Sword):
    #name = "Orcish Dagger"
    #weight = 10
    #min_dungeon_level = 2
    #def on_wield_attack(self, wielder, target):
        #wielder.strength_bonus += 0.005
        #return target.damage(max(1, wielder.strength/1.3))

#class DrinkingCanSword(Sword):
    #name = "Lemonade Can Sword"
    #weight = 3
    #min_dungeon_level = 4
    #def on_wield_attack(self, wielder, target):
        #wielder.strength_bonus += 0.005
        #return target.damage(max(1, wielder.strength))

#class GlowingIronSword(Sword):
    #name = "Glowing Iron Sword"
    #weight = 3
    #min_dungeon_level = 9
    #def on_wield_attack(self, wielder, target):
        #wielder.strength_bonus += 0.02
        #if wielder.mana > 10:
            #wielder.mana -= 10
            #magic_bonus = wielder.spirit * 3
            #wielder.spirit_bonus += 0.005
        #else:
            #magic_bonus = 0
        #return target.damage(max(1, wielder.strength*2 + wielder.spirit_bonus))
