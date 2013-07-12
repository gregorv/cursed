
from __future__ import division

import random
import math
import itertools
import curses

from item import Pile, Container, ItemRegistry
#import character
#from registry import NPCRegistry, ItemRegistry

class Map:
    def __init__(self, game, name, size):
        self.game = game
        self.name = name
        self.size = size
        self.npc_list = []
        self.item_piles = {}
        self.particle_list = []
        self.stairs = []
        self.data = []
        self.data_wall = []
        self.data_water = []
        self.discovered = [[" "]*self.size[0] for i in range(self.size[1])]
        self._visible_area = []

    def update(self):
        self._update_discovery()
        self.item_piles = dict(filter(lambda x: len(x[1].items) > 0,
                                      self.item_piles.items()))

    def _update_discovery(self):
        self._visible_area = self.get_visible_area(self.game.player.pos, 8)
        for x,y in self._visible_area:
            self.discovered[y][x] = self.data_floor[y][x]

    def get_los_fields(self, start, end):
        """
        Return a generator for field coordinates that are in
        the line of sight from start to end.
        No occlusion checks are done!
        """
        diff = (end[0]-start[0], end[1]-start[1])
        max_grid_dist = max(*map(abs, diff))
        if max_grid_dist == 0:
            yield start
        else:
            delta = (diff[0]/max_grid_dist,
                     diff[1]/max_grid_dist)
            fields = [start]
            cur = start
            while(end[0] != int(round(cur[0]))
                or end[1] != int(round(cur[1]))):
                cur = (cur[0]+delta[0], cur[1]+delta[1])
                yield int(round(cur[0])), int(round(cur[1]))

    def get_occluded_los_fields(self, start, end):
        """
        Return a generator for field coordinates that are in
        the line of sight from start to end. If something
        is in the way (#), the list is aborted. The occluding
        field is included in the list!
        """
        for pos in self.get_los_fields(start, end):
            yield pos
            if self.data_floor[pos[1]][pos[0]] == "#":
                break

    def get_field_circle(self, center, radius):
        """
        A generator returning field coordinates that lie on
        the specified circle. Note that a squared metric is used!
        """
        prev_y = 0
        recalc_y = 0
        for x in range(-radius, radius+1):
            y = int(round(math.sqrt(radius**2 - x**2)))
            if prev_y - y > 1 and recalc_y == 0:
                recalc_y = prev_y
            yield (center[0]+x, center[1]+y)
            yield (center[0]+x, center[1]-y)
            prev_y = y
        for y in range(-recalc_y+1, recalc_y):
            x = int(round(math.sqrt(radius**2 - y**2)))
            yield (center[0]+x, center[1]+y)
            yield (center[0]-x, center[1]+y)

    def get_visible_area(self, center, radius):
        """
        return a list of all field positions that are visible from the given center point.
        Visible means that it a field is both inside the given radius and the los is
        not occluded by the dungeon ("#")
        """
        visible = set()
        closed_circle = set(self.get_field_circle(center, radius))
        closed_circle.update(set(self.get_field_circle(center, radius-1)))
        for p in closed_circle:
            visible.update(set(self.get_occluded_los_fields(center, p)))
        return list(visible)

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
        if self.data_floor[pos[1]][pos[0]] == "#":
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
        
    def generate(self):
        self.data_floor = [["#"]*self.size[0]]
        self.data_floor.extend([["#"]+["."]*(self.size[0]-2)+["#"] for i in range(self.size[1]-2)])
        self.data_floor.append(["#"]*self.size[0])
    
    def populate(self, n=10):
        pass
    
    def on_enter(self, origin):
        for npc in self.npc_list:
            npc.last_know_player_pos = None
    
    def on_exit(self, target):
        pass
        
    def render(self, scr, topleft_offset, scrdim, center=None):
        if center is None:
            center = self.game.player.pos
        scrmid = (scrdim[0]//2 + topleft_offset[0],
                  scrdim[1]//2 + topleft_offset[1])
        # word coord -> screen coord
        coord = lambda pos: (pos[1]-center[1]+scrmid[0],
                             pos[0]-center[0]+scrmid[1])
        # screen coord > wordl coord
        revcoord = lambda pos: (pos[1]+center[0]-scrmid[1],
                             pos[0]+center[1]-scrmid[0])

        player_pos = coord(self.game.player.pos)

        in_scr = lambda pos:(pos[0] >= topleft_offset[0]
                             and pos[1] >= topleft_offset[1]
                             and pos[0] < scrdim[0]
                             and pos[1] < scrdim[1])
        
        # draw map
        sty_wall = self.game.style["map.wall"]
        sty_wall_vis = self.game.style["map.wall_visible"]
        sty_floor = self.game.style["map.floor"]
        sty_floor_vis = self.game.style["map.floor_visible"]
        sty_water = self.game.style["map.water"]
        sty_water_vis = self.game.style["map.water_visible"]
        sty_misc = self.game.style["map.misc"]
        sty_misc_vis = self.game.style["map.misc_visible"]
        for ys in range(topleft_offset[0], topleft_offset[0]+scrdim[0]):
            pos = revcoord((ys, topleft_offset[1]))
            if pos[1] < 0 or pos[1] >= self.size[1]:
                continue
            for xs in range(topleft_offset[1], topleft_offset[1]+scrdim[1]):
                x, y = revcoord((ys, xs))
                if x < 0 or x >= self.size[0]:
                    continue
                if self.discovered[y][x] == ".":
                    scr.addch(ys, xs,
                               ".",
                                sty_floor_vis if (x,y) in self._visible_area else sty_floor
                                )
                elif self.discovered[y][x] == "#":
                    scr.addch(ys, xs,
                               "#",
                               sty_wall_vis if (x,y) in self._visible_area else sty_wall
                               )
                elif self.discovered[y][x] == "~":
                    scr.addch(ys, xs,
                               "~",
                               sty_water_vis if (x,y) in self._visible_area else sty_water
                               )
                else:
                    scr.addch(ys, xs,
                               self.discovered[y][x],
                                sty_misc_vis if (x,y) in self._visible_area else sty_misc
                                )
        # draw item piles
        for pos, pile in self.item_piles.items():
            scrcoord = coord(pos)
            if in_scr(scrcoord):
                if(pos not in self._visible_area
                   and self.discovered[pos[1]][pos[0]] == " "):
                    continue
                scr.addch(scrcoord[0], scrcoord[1],
                           pile.render(),
                           curses.A_DIM)
        # draw NPCs (only if in view)
        for pos, pile in self.item_piles.items():
            scrcoord = coord(pos)
            if in_scr(scrcoord) and pos in self._visible_area:
                scr.addch(scrcoord[0], scrcoord[1],
                           pile.render())
        if in_scr(player_pos):
            scr.addch(player_pos[0], player_pos[1], "@", self.game.style["player"])
        #fileds = self.get_field_circle(self.game.player.pos, 8)
        #for p in map(coord, fileds):
           #if in_scr(p):
                #scr.addch(p[0], p[1], "*", curses.color_pair(1))
        
class RandomDungeon(Map):
    def generate(self):
        self.data_floor = [["#"]*self.size[0]]
        self.data_floor.extend([["#"]+["."]*(self.size[0]-2)+["#"] for i in range(self.size[1]-2)])
        self.data_floor.append(["#"]*self.size[0])
        for i in range(600):
            x = random.randint(4, self.size[0]-4)
            y = random.randint(4, self.size[1]-4)
            self.data_floor[y][x] = "#"
            self.data_floor[y+1][x] = "#"
            self.data_floor[y][x+1] = "#"
            self.data_floor[y+1][x+1] = "#"