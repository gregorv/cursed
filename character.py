
import math
import random
import spell
from registry import NPCRegistry

class Character:
    def __init__(self, game):
        self.game = game
        self.inventory = {}
        self.spells = {}
        self.max_hp = 100
        self.max_mana = 100
        self.hp = 30
        self.mana = 10
        self.strength = 0
        self.spirit = 0
        self.regen = 0
        self.mana_regen = 0
        self.hp_bonus = 0
        self.mana_regen_bonus = 0
        self.mana_bonus = 0
        self.strength_bonus = 0
        self.spirit_bonus = 0
        self.regen_bonus = 0
        self.in_hands = None
        self.armour = None
        self.last_enemy = None
        self.level = 1
        self.x = 1
        self.y = 1
        
    def damage(self, dmg):
        self.hp = max(0, self.hp-int(dmg))
        if not self.hp:
            self.kill()
            return True
        else:
            return False
    
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
        self.level = int(level)
        self.loot = loot
    
    #def death_message(self):
        #self.game.logger.log("You killed the {0}".format(self.__class__.__name__))

class NPCEnemy(NPC):
    def __init__(self, game, level, loot):
        NPC.__init__(self, game, level, loot)
        self.last_know_player_pos = None
    
    def attack(self, target):
        target.damage(10)
        self.last_know_player_pos = None
        self.view_range = 6
        
    def animate(self):
        self.hp = int(min(self.max_hp, self.hp + self.regen))
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
        if dist < self.view_range:
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

class NPCEnemyMagican(NPCEnemy):
    def __init__(self, game, level, loot):
        NPCEnemy.__init__(self, game, level, loot)
        self.next_spell = None
        self.spells = []
        self.spirit = int(level*2.3)
        
    def attack(self, target):
        target.damage(self.level)
    
    def cast(self, target):
        self.game.logger.log("The {0} casts {1}".format(self.name, self.next_spell))
        spell.trigger_action(self.next_spell,
                             self.game,
                             self,
                             target,
                             (target.x, target.y),
                             silent=True)
        self.next_spell = random.choice(self.spells)
        
    def animate(self):
        self.hp = int(min(self.max_hp, self.hp + self.regen))
        self.mana = int(min(self.max_mana, self.mana + self.mana_regen))
        
        if self.spells and not self.next_spell:
            self.next_spell = random.choice(self.spells)
        
        neighbourhood = [(self.x-1, self.y-1),
                         (self.x, self.y-1),
                         (self.x+1, self.y-1),
                         (self.x-1, self.y),
                         (self.x+1, self.y),
                         (self.x-1, self.y+1),
                         (self.x, self.y+1),
                         (self.x+1, self.y+1),
                        ]
        
        dist = math.sqrt((self.game.player.x - self.x)**2
                         + (self.game.player.y - self.y)**2)
        
        player_in_view = dist < self.view_range
        health_critical = self.hp/self.max_hp < 0.1
        sufficient_mana = (spell.spell_list[self.next_spell]["mana"] <= self.mana)
        magic_in_range = True
        if spell.spell_list[self.next_spell]["range"]:
            magic_in_range = dist < spell.spell_list[self.next_spell]["range"]
            
        if player_in_view:
            self.last_know_player_pos = self.game.player.x, self.game.player.y
        
        if magic_in_range and sufficient_mana:
            self.cast(self.game.player)
        elif player_in_view and health_critical:
            self.next_spell = "blink"
        elif self.last_know_player_pos:
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
        else:
            for pos in neighbourhood:
                if(pos[0] == self.game.player.x
                and pos[1] == self.game.player.y):
                    self.attack(self.game.player)
                    return
class Ant(NPCEnemy):
    name = "Ant"
    symbol = "a"
    min_dungeon_level = 1
    max_dungeon_level = 4
    
    def __init__(self, game, loot):
        NPCEnemy.__init__(self, game, random.randint(1, 3), loot)
        self.max_hp = 3+self.level
        self.hp = self.max_hp
        self.view_range = 4
        
    def exp_loot(self):
        return self.level*4
    
    def attack(self, target):
        target.damage(self.level)


class Ferret(NPCEnemy):
    name = "Ferret"
    symbol = "f"
    min_dungeon_level = 2
    max_dungeon_level = 6
    
    def __init__(self, game, loot):
        NPCEnemy.__init__(self, game, random.randint(1, 3), loot)
        self.max_hp = 5+self.level**2
        self.hp = self.max_hp
        self.view_range = 4
        
    def exp_loot(self):
        return int(self.level*5.5)
    
    def attack(self, target):
        target.damage(self.level*1.5)

class PorkWarrior(NPCEnemy):
    name = "Pork Warrior"
    symbol = "p"
    min_dungeon_level = 3
    max_dungeon_level = 7
    
    def __init__(self, game, loot):
        level = min(5, max(1, random.gauss(1, 5)))
        NPCEnemy.__init__(self, game, level, loot)
        self.max_hp = int(20+7*level**1.4)
        self.hp = self.max_hp
        self.regen = 1
        self.view_range = 7
        
    def exp_loot(self):
        return self.level*70
    
    def attack(self, target):
        target.damage(self.level**0.5*10)


class BeefCaster(NPCEnemyMagican):
    name = "Beef Caster"
    symbol = "B"
    min_dungeon_level = 5
    max_dungeon_level = 10
    
    def __init__(self, game, loot):
        level = min(5, max(1, random.gauss(4, 4)))
        NPCEnemyMagican.__init__(self, game, level, loot)
        self.spells = ["fire", "fire", "fire", "fire"]
        self.spirit = 15*self.level
        if self.spirit >= 7:
            self.spells.append("firestorm")
        self.max_hp = int(40+6*level**1.4)
        self.hp = self.max_hp
        self.hp_regen = level
        self.max_mana = int(self.level*400/8)
        self.mana = self.max_mana
        self.mana_regen = 10*self.level
        self.view_range = 8
        
    def exp_loot(self):
        return self.level**2 * 50 + 300
    

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
        self.mana_regen = 0
        self.hp_bonus = 0
        self.mana_regen_bonus = 0
        self.mana_bonus = 0
        self.strength_bonus = 0
        self.spirit_bonus = 0
        self.regen_bonus = 0
        self.in_hands = None
        self.armour = None
        self.last_enemy = None
        
        self.level = 0 # force recalculation in apply_exp()
        self.apply_exp()
        self.items = {}
        self.spells = ["firestorm","blink", "heal", "fire", "softdestruct"]
        
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
        self.last_enemy = target
        enemy_killed = False
        if self.in_hands:
            enemy_killed = self.in_hands.on_wield_attack(self, target)
            if self.in_hands.destroyed:
                self.items[self.in_hands.name] -= 1
                if self.items[self.in_hands.name] == 0:
                    del self.items[self.in_hands.name]
                    self.in_hands = None
        else:
            enemy_killed = target.damage(1)
        if enemy_killed:
            self.exp += int(target.exp_loot())
            self.apply_exp()
            self.game.logger.log("You killed the "+str(target.name))
    
    def death_message(self):
        self.game.logger.log("You die.")
        
    def apply_exp(self):
        cur_level = self.level
        self.level = Player.exp_formula(self.exp)
        lvl_diff = self.level-cur_level
        if lvl_diff > 0:
            self.max_hp = int(20 + 10*self.level**1.7) + self.hp_bonus
            self.max_mana = int(10*self.level**1.9 + self.mana_bonus)
            self.strength = int(self.level + (self.level/4.0)**4 + self.strength_bonus)
            self.spirit = int(self.level + (self.level/4.0)**4 + self.spirit_bonus)
            self.regen = int(self.level*1.9 + self.regen_bonus)
            self.mana_regen = int(1 + 0.4*self.level**2 + self.mana_regen_bonus)
            
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