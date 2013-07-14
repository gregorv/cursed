""
from __future__ import division
"""
    This file is part of Cursed
    Copyright (C) 2013 Gregor Vollmer <gregor@celement.de>

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import math
import random

from registry import Registry
from entity import Entity
import fightsystem


class NPCRegistry(Registry):
    @classmethod
    def create(cls, game, npc):
        return cls.classes[npc](game)

    @classmethod
    def check_validity(cls, name, bases, dict):
        return("name" in dict
               and "view_range" in dict
               and "attack_power" in dict)


class NPC(Entity):
    __metaclass__ = NPCRegistry

    def __init__(self, game):
        Entity.__init__(self, game)
        self.last_known_player_pos = None
        self.random_target = None
        self.name = self.__class__.name
        self.attack_power = self.__class__.attack_power
        self.view_range = self.__class__.view_range

    def attack_enemy(self, target):
        target.hp = int(max(0, target.hp - self.attack_power))

    def animate(self):
        if self.random_target is not None:
            dist = ((self.random_target[0] - self.pos[0])**2
                    + (self.random_target[1] - self.pos[1])**2)
            if dist < 6:
                self.random_target = None
        if self.last_known_player_pos is not None:
            dist = ((self.last_known_player_pos[0] - self.pos[0])**2
                    + (self.last_known_player_pos[1] - self.pos[1])**2)
            if dist < 2:
                self.last_known_player_pos = None
        if self.random_target is None:
            self.random_target = (random.randint(self.pos[0]-10, self.pos[0]+10),
                                  random.randint(self.pos[1]-10, self.pos[1]+10))
            self.random_target = list(self.game.map.get_occluded_los_fields(self.pos, self.random_target))[-1]

        neighbourhood = [(self.pos[0]-1, self.pos[1]-1),
                         (self.pos[0], self.pos[1]-1),
                         (self.pos[0]+1, self.pos[1]-1),
                         (self.pos[0]-1, self.pos[1]),
                         (self.pos[0]+1, self.pos[1]),
                         (self.pos[0]-1, self.pos[1]+1),
                         (self.pos[0], self.pos[1]+1),
                         (self.pos[0]+1, self.pos[1]+1),
                         ]
        for pos in neighbourhood:
            if pos == self.game.player.pos:
                self.attack_enemy(self.game.player)
                self.set_round_cooldown(10)
                return

        dist = ((self.game.player.pos[0] - self.pos[0])**2
                + (self.game.player.pos[1] - self.pos[1])**2)
        if dist < self.view_range**2:
            if self.game.map.get_los_unblocked(self.pos, self.game.player.pos):
                self.last_known_player_pos = self.game.player.pos

        target = (self.last_known_player_pos
                  if self.last_known_player_pos is not None
                  else self.random_target
                  )
        if target is not None:
            diff_x = target[0] - self.pos[0]
            diff_y = target[1] - self.pos[1]
            if diff_x != 0: diff_x = diff_x // abs(diff_x)
            if diff_y != 0: diff_y = diff_y // abs(diff_y)
            movements = [
                         (diff_x, diff_y),
                         (diff_x, 0),
                         (0, diff_y),
                         ]
            random.shuffle(movements)
            for m in movements:
                new_x = m[0] + self.pos[0]
                new_y = m[1] + self.pos[1]
                if not self.game.map.collision_detect((new_x, new_y)):
                    self.pos = (new_x, new_y)
                    self.set_round_cooldown(10)
                    return
            for m in movements:
                new_x = -m[0] + self.pos[0]
                new_y = -m[1] + self.pos[1]
                if not self.game.map.collision_detect((new_x, new_y)):
                    self.pos = (new_x, new_y)
                    self.set_round_cooldown(10)
                    return


class Ant(NPC):
    name = "Ant"
    view_range = 4
    attack_power = 5

    def __init__(self, game):
        NPC.__init__(self, game)
        self.style = self.game.style["player"]
        self.hp = 10
        self.symbol = "a"
