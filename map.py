
import random
import math
import itertools

from item import Pile, Container, ItemRegistry
#import character
#from registry import NPCRegistry, ItemRegistry

class Map:
    def __init__(self, game, name):
        self.game = game
        self.name = name
        self.size = (int(self.game.config["map"]["width"]),
                     int(self.game.config["map"]["height"]))
        self.npc_list = []
        self.item_piles = {}
        self.particle_list = []
        self.stairs = []
        self.data = [["#"]*self.size[0]]
        self.data.extend([["#"]+["."]*(self.size[0]-2)+["#"] for i in range(self.size[1]-2)])
        self.data.append(["#"]*self.size[0])
        for i in range(200):
            x = random.randint(1, self.size[0]-2)
            y = random.randint(1, self.size[1]-2)
            self.data[y][x] = "a"
        
    def add_items(self, items, pos):
        if pos not in self.item_piles:
            self.item_piles[pos] = Pile(self.game, self, pos)
        self.item_piles[pos].add(items)
        
    def pop_items(self, pos):
        items = Container(self, self.game)
        if pos in self.item_piles:
            items.add(self.item_piles[pos])
            del self.item_piles[pos]
        return items
        
    #def update(self):
        #def removeKilledNPCs():
            #killed = list(filter(lambda npc: npc.hp <= 0, self.npc_list))
            #for npc in killed:
                #for item in npc.loot:
                    #self.item_list.append((npc.x, npc.y, item))
        #removeKilledNPCs()
        #for npc in self.npc_list:
            #npc.animate()
        #for p in self.particle_list:
            #p.animate()
            #other = self.collision_detect(p.x, p.y)
            #if isinstance(other, character.Character):
                #p.on_character_touch(other)
            #p.lifetime -= 1
        #self.particle_list = list(filter(lambda p: p.lifetime > 0, self.particle_list))
        #removeKilledNPCs()
        #self.npc_list = list(filter(lambda npc: npc.hp > 0, self.npc_list))
        
    def collision_detect(self, pos, ignore=None):
        if(pos[0] >= self.size[0] or pos[1] >= self.size[1]
           or pos[0] < 0 or pos[1] < 0):
            return "dungeon"
        if self.data[pos[1]][pos[0]] == "#":
            return "dungeon"
        #if(self.pos_stairs_in
           #and (x == self.pos_stairs_in[0]
           #and y == self.pos_stairs_in[1])):
            #return "<"
        #if(self.pos_stairs_out
           #and (x == self.pos_stairs_out[0]
           #and y == self.pos_stairs_out[1])):
            #return ">"
        #for npc in self.npc_list:
            #if npc == ignore:
                #continue
            #if x == npc.x and y == npc.y:
                #return npc
        if pos == self.game.player.pos:
            return self.game.player
        return None
    
    def get_free_space(self):
        while True:
            x = random.randint(0, self.size[0])
            y = random.randint(0, self.size[1])
            if self.collision_detect((x, y)) is None:
                return (x, y)
        
    #def generate(self):
        #self.populate(20)
    
    #def populate(self, n=10):
        #select = lambda n: (n.min_dungeon_level<=self.level
                            #and n.max_dungeon_level>=self.level)
        #npc_classes = list(filter(select, NPCRegistry.npc_classes))
        #loot_classes = ItemRegistry.names_upto_dungeonlevel(self.level)
        #for i in range(n):
            #level = int(max(1, random.gauss(self.level, 2.5)))
            #cls = random.choice(npc_classes)
            #num_loot_items = min(2, max(0, int(random.gauss(0, 2))))
            #loot = [random.choice(loot_classes) for i in range(num_loot_items)]
            #npc = cls(self.game, loot)
            #npc.x, npc.y = self.get_free_space()
            #self.npc_list.append(npc)
    
    #def on_enter(self, origin):
        #if len(self.npc_list) < 20:
            #self.populate(3)
        #for npc in self.npc_list:
            #npc.last_know_player_pos = None
    
    #def on_exit(self, target):
        #pass
        
    def render(self, scr, topleft_offset, scrdim):
        player_pos = self.game.player.pos
        scrmid = (scrdim[0]//2 + topleft_offset[0],
                  scrdim[1]//2 + topleft_offset[1])
        coord = lambda pos: (pos[1]-player_pos[1]+scrmid[0],
                             pos[0]-player_pos[0]+scrmid[1])
        revcoord = lambda pos: (pos[1]+player_pos[0]-scrmid[1],
                             pos[0]+player_pos[1]-scrmid[0])
        in_scr = lambda pos:(pos[0] >= topleft_offset[0]
                             and pos[1] >= topleft_offset[1]
                             and pos[0] < scrdim[0]
                             and pos[1] < scrdim[1])
      
        
        # draw map
        for y in range(topleft_offset[0], topleft_offset[0]+scrdim[0]):
            pos = revcoord((y, topleft_offset[1]))
            real_y = max(0, min(self.size[1]-1, pos[1]))
            start_x = max(0, pos[0])
            end_x = min(pos[0]+scrdim[1], self.size[0])
            if pos[1] < 0 or pos[1] >= self.size[1]:
                continue
            x = topleft_offset[1]+max(0, -pos[0]+start_x)
            scr.addstr(y, x, "".join(self.data[real_y][start_x:end_x]))
        
        # draw item piles
        for pos, pile in self.item_piles.items():
            scrcoord = coord(pos)
            if in_scr(scrcoord):
                scr.addch(scrcoord[0], scrcoord[1],
                           pile.render())
            
        scr.addch(scrmid[0], scrmid[1], "@")
        
