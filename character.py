
import math
import random
from registry import NPCRegistry

class Character:
    def __init__(self, game):
        self.game = game
        self.inventory = {}
        self.spells = {}
        self.max_hp = 100
        self.max_mana = 100
        self.hp = 100
        self.mana = 100
        self.level = 1
        self.x = 1
        self.y = 1
        
    def damage(self, dmg):
        self.hp = max(0, self.hp-int(dmg))
        if not self.hp:
            self.kill()
    
    def heal(self, hp):
        self.hp = min(self.max_hp, self.hp+int(hp))
            
    def kill(self, msg=None):
        self.hp = 0
        if msg:
            self.game.logger.log(msg)
        self.death_message()
        
    def death_message(self):
        pass
            

class NPC(Character, metaclass=NPCRegistry):
    def __init__(self, game, level, loot):
        Character.__init__(self, game)
        self.level = level
        self.loot = loot
    
    def death_message(self):
        self.game.logger.log("You killed the {0}".format(self.__class__.__name__))

class NPCEnemy(NPC):
    def attack(self, target):
        target.damage(10)
        self.last_know_player_pos = None
        
    def animate(self):
        neighbourhood = [(self.x-1, self.y-1),
                         (self.x, self.y-1),
                         (self.x+1, self.y-1),
                         (self.x-1, self.y),
                         (self.x+1, self.y),
                         (self.x-1, self.y+1),
                         (self.x, self.y+1),
                         (self.x+1, self.y+1),
                        ]
        for pos in neighbourhood:
            if(pos[0] == self.game.player.x
               and pos[1] == self.game.player.y):
                self.attack(self.game.player)
                return
            
        dist = math.sqrt((self.game.player.x - self.x)**2
                         + (self.game.player.y - self.y)**2)
        if dist < 6:
            self.last_know_player_pos = self.game.player.x, self.game.player.y
        
        if self.last_know_player_pos:
            diff_x = self.game.player.x - self.x
            diff_y = self.game.player.y - self.y
            if diff_x != 0: diff_x = int(diff_x / abs(diff_x))
            if diff_y != 0: diff_y = int(diff_y / abs(diff_y))
            movements = [
                (diff_x, diff_y),
                (diff_x, 0),
                (0, diff_y),
               ]
            random.shuffle(movements)
            for m in movements:
                new_x = m[0] + self.x
                new_y = m[1] + self.y
                if not self.game.dungeon.cur_dungeon.collision_detect(new_x, new_y):
                    self.x = new_x
                    self.y = new_y
                    return
            
            for m in movements:
                new_x = -m[0] + self.x
                new_y = -m[1] + self.y
                if not self.game.dungeon.cur_dungeon.collision_detect(new_x, new_y):
                    self.x = new_x
                    self.y = new_y
                    return

class Ferret(NPCEnemy):
    name = "Ferret"
    symbol = "f"
    min_dungeon_level = 1
    
    def __init__(self, game, level, loot):
        NPCEnemy.__init__(self, game, level, loot)
        self.max_hp = 3+level**2
        self.hp = self.max_hp
        
    def exp_loot(self):
        return self.level*4
    
    def attack(self, target):
        target.damage(self.level)
        
class NPCDummy(NPC):
    pass

class Player(Character):
    exp_formula = lambda exp: int(math.log(exp/30+1)) + 1
    
    def __init__(self, game):
        Character.__init__(self, game)
        self.exp = 0
        self.strength = 0
        self.spirit = 0
        self.regen = 0
        self.mana_bonus = 0
        self.strength_bonus = 0
        self.spirit_bonus = 0
        self.regen_bonus = 0
        self.in_hands = None
        self.armour = None
        
        self.level = 0 # force recalculation in apply_exp()
        self.apply_exp()
        self.items = {}
        
    def add_items(self, item_list):
        if hasattr(item_list, "__next__"):
            item_list = [item_list]
        for item in item_list:
            if hasattr(item, "name"):
                item = item.name
            if item in self.items:
                self.items[item] += 1
            else:
                self.items[item] = 1
    
    def attack(self, target):
        if self.in_hands:
            self.in_hands.on_wield_attack(self, target)
            if self.in_hands.destroyed:
                self.items[self.in_hands.name] -= 1
                if self.items[self.in_hands.name] == 0:
                    del self.items[self.in_hands.name]
                    self.in_hands = None
        else:
            target.damage(1)
    
    def death_message(self):
        self.game.logger.log("You die.")
        
    def apply_exp(self):
        cur_level = self.level
        self.level = Player.exp_formula(self.exp)
        lvl_diff = self.level-cur_level
        if lvl_diff > 0:
            self.max_hp = int(20 + 10*self.level**1.7)
            self.max_mana = int(90 + 10*self.level**1.9 + self.mana_bonus)
            self.strength = int(self.level + (self.level/4.0)**4 + self.strength_bonus)
            self.spirit = int(self.level + (self.level/4.0)**4 + self.spirit_bonus)
            self.regen = int(self.level*1.3 + self.regen_bonus)
            
            # binary-search where next lvl is
            start = self.exp
            stop = 2 + self.exp**2
            while Player.exp_formula(stop) == self.level:
                stop = stop**2
            self.exp_next_level = stop
            while Player.exp_formula(self.exp_next_level) \
                == Player.exp_formula(self.exp_next_level-1):
                self.exp_next_level = start + int(math.ceil((stop-start)/2))
                if Player.exp_formula(self.exp_next_level) > self.level:
                    stop = self.exp_next_level
                else:
                    start = self.exp_next_level