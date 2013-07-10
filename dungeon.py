
import random
import math

import item
import character
from registry import NPCRegistry, ItemRegistry

class Dungeon:
    def __init__(self, game, level, max_x, max_y):
        self.game = game
        self.level = level
        self.max_x = max_x
        self.max_y = max_y
        self.npc_list = []
        self.item_list = []
        self.particle_list = []
        
        self.pos_stairs_in = (random.randint(2, max_x-2), random.randint(2, max_y-2))
        if self.level == 1:
            self.pos_stairs_in = None
        while True:
            self.pos_stairs_out = (random.randint(2, max_x-2),
                                   random.randint(2, max_y-2))
            if not self.pos_stairs_in:
                break
            dist = (self.pos_stairs_out[0]-self.pos_stairs_in[0])**2
            dist += (self.pos_stairs_out[1]-self.pos_stairs_in[1])**2
            dist = math.sqrt(dist)
            if dist > 6:
                break
    
    def pop_items(self, x, y):
        items = [it[2] for it in self.item_list if it[0] == x and it[1] == y]
        self.item_list = [it for it in self.item_list if it[0] != x or it[1] != y]
        return items
        
    def update(self):
        for npc in self.npc_list:
            npc.animate()
        for p in self.particle_list:
            p.animate()
            other = self.collision_detect(p.x, p.y)
            if isinstance(other, character.Character):
                p.on_character_touch(other)
            p.lifetime -= 1
        self.particle_list = list(filter(lambda p: p.lifetime > 0, self.particle_list))
        killed = list(filter(lambda npc: npc.hp <= 0, self.npc_list))
        for npc in killed:
            for item in npc.loot:
                self.item_list.append((npc.x, npc.y, item))
        self.npc_list = list(filter(lambda npc: npc.hp > 0, self.npc_list))
        
    def collision_detect(self, x, y, ignore=None):
        if(x >= self.max_x-1 or y >= self.max_y-1
           or x < 1 or y < 1):
            return "dungeon"
        #if(self.pos_stairs_in
           #and (x == self.pos_stairs_in[0]
           #and y == self.pos_stairs_in[1])):
            #return "<"
        #if(self.pos_stairs_out
           #and (x == self.pos_stairs_out[0]
           #and y == self.pos_stairs_out[1])):
            #return ">"
        for npc in self.npc_list:
            if npc == ignore:
                continue
            if x == npc.x and y == npc.y:
                return npc
        if(x == self.game.player.x
           and y == self.game.player.y):
            return self.game.player
        return None
    
    def get_free_space(self):
        while True:
            x = random.randint(1, self.max_x-2)
            y = random.randint(1, self.max_y-2)
            if self.collision_detect(x, y) is None:
                return (x, y)
        
    def generate(self):
        self.populate(20)
    
    def populate(self, n=10):
        select = lambda n: (n.min_dungeon_level<=self.level
                            and n.max_dungeon_level>=self.level)
        npc_classes = list(filter(select, NPCRegistry.npc_classes))
        loot_classes = ItemRegistry.names_upto_dungeonlevel(self.level)
        for i in range(n):
            level = int(max(1, random.gauss(self.level, 2.5)))
            cls = random.choice(npc_classes)
            num_loot_items = min(2, max(0, int(random.gauss(0, 2))))
            loot = [random.choice(loot_classes) for i in range(num_loot_items)]
            npc = cls(self.game, loot)
            npc.x, npc.y = self.get_free_space()
            self.npc_list.append(npc)
    
    def on_enter(self):
        if len(self.npc_list) < 20:
            self.populate(3)
        for npc in self.npc_list:
            npc.last_know_player_pos = None
    def on_exit(self):
        pass
        
    def render(self, scr):
        for y in range(1, self.max_y-1):
            scr.addstr(y, 1, "."*(self.max_x-2))
        if self.pos_stairs_in:
            scr.addch(self.pos_stairs_in[1], self.pos_stairs_in[0], "<")
        scr.addch(self.pos_stairs_out[1], self.pos_stairs_out[0], ">")
        for x, y, item in self.item_list:
            scr.addch(y, x, ItemRegistry.by_name(item).symbol)
        scr.addch(self.game.player.y,
                       self.game.player.x,
                       "@")
        for npc in self.npc_list:
            scr.addch(npc.y, npc.x, npc.symbol)
        for p in self.particle_list:
            p.render(scr)