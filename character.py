
import math

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

class NPC(Character):
    def __init__(self, game, level):
        Character.__init__(self, game)
        self.level = level
        self.min_dungeon_level = 1
        
    def animate(self):
        pass
        
class NPCDummy(NPC):
    pass

class Player(Character):
    exp_formula = lambda exp: int(math.log(exp/30+1)) + 1
    
    def __init__(self, game):
        Character.__init__(self, game)
        self.exp = 0
        self.strength = 0
        self.spirit = 0
        self.mana_bonus = 0
        self.strength_bonus = 0
        self.spirit_bonus = 0
        self.in_hands = None
        self.armour = None
        
        self.level = 0 # force recalculation in apply_exp()
        self.apply_exp()
    
    def apply_exp(self):
        cur_level = self.level
        self.level = Player.exp_formula(self.exp)
        lvl_diff = self.level-cur_level
        if lvl_diff > 0:
            self.max_hp = int(90 + 10*self.level**1.7)
            self.max_mana = int(90 + 10*self.level**1.9 + self.mana_bonus)
            self.strength = int(self.level + (self.level/4.0)**4 + self.strength_bonus)
            self.spirit = int(self.level + (self.level/4.0)**4 + self.spirit_bonus)
            
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