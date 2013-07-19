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

from entity import Entity, SkillSet
from item import Inventory
import math
import fightsystem
import json
import playerdefs


class Player(Entity):
    def __init__(self, game):
        Entity.__init__(self, game)
        self.mana = 0
        self.skills = SkillSet()
        self.inventory = Inventory(self.game)
        self.wielded = None
        self.symbol = "@"
        self.style = self.game.style["player"]
        self.exp = 0
        self.level_skills = ["char.hp"]

    def pre_round(self):
        Entity.pre_round(self)
        self.effective_skills.replace_levels(self.skills)

    def exp_next_level(self):
        return 1000

    def exp_this_level(self):
        return self.exp % self.exp_next_level()

    def attack(self, target):
        if self.wielded:
            self.wielded.on_wield_attack(target)
        else:
            dmg = fightsystem.standard_physical(self,
                                                target,
                                                5,
                                                None)
            dmg = fightsystem.status_effect(self, target, dmg)
            target.hp = int(max(0, target.hp - dmg))
        self.set_round_cooldown(10)
        if target.hp <= 0 and (self.level - target.level) < 15:
            self.exp += int(150*math.exp(-0.2*(self.level - target.level)))
            self.level_up()

    def level_up(self):
        exp_level = (self.exp // self.exp_next_level()) + 1
        # loop for multiple levelups (extremely many exp?!)
        while self.level < exp_level:
            self.level += 1
            exp_per_skill = int(round(1000/len(self.level_skills)))
            for skill in self.level_skills:
                self.skills.add_exp(skill, exp_per_skill)

    def handle_keypress(self, code, mod):
        move = (0, 0)
        if self.game.keymap("player.w", code, mod): move = (-1, 0)
        elif self.game.keymap("player.e", code, mod): move = (1, 0)
        elif self.game.keymap("player.n", code, mod): move = (0, -1)
        elif self.game.keymap("player.s", code, mod): move = (0, 1)
        elif self.game.keymap("player.ne", code, mod): move = (1, -1)
        elif self.game.keymap("player.nw", code, mod): move = (-1, -1)
        elif self.game.keymap("player.se", code, mod): move = (1, 1)
        elif self.game.keymap("player.sw", code, mod): move = (-1, 1)
        elif self.game.keymap("player.wait", code, mod):
            self.set_round_cooldown(10)
        elif self.game.keymap("player.pickup", code, mod):
            if self.pos in self.game.map.item_piles:
                self.game.set_view("PickupItems",
                                   self.game.map.item_piles[self.pos])
        else:
            return False

        if move != (0, 0):
            new = move[0] + self.pos[0], move[1] + self.pos[1]
            detect = self.game.map.collision_detect(new)
            if detect is None:
                self.pos = new
                self.set_round_cooldown(math.sqrt((10*move[0])**2
                                                  + (10*move[1])**2))
            elif isinstance(detect, Entity):
                self.attack(detect)
        return True


def create_player(game, race, cls):
    player = Player(game)
    if race:
        player.skills.add_base_definition(playerdefs.race_def[race])
    if cls:
        player.skills.add_base_definition(playerdefs.class_def[cls])
    player.hp = player.skills["char.hp"]
    player.mana = player.skills["char.mana"]
    player.effective_skills.replace_levels(player.skills)
    return player
