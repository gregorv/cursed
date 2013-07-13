""
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

import curses
import random

class Particle:
    def __init__(self, game, x, y, lifetime):
        self.game = game
        self.x = int(x)
        self.y = int(y)
        self.lifetime = int(lifetime)
        self.game.dungeon.cur_dungeon.particle_list.append(self)
    
    def animate(self):
        pass
    
    def on_character_touch(self, character):
        pass
    
    def render(self, scr):
        scr.chgat(self.y, self.x, 1, curses.color_pair(1))

class Fire(Particle):
    def __init__(self, game, x, y, lifetime, damage, sigma, mobile):
        Particle.__init__(self, game, x, y, lifetime)
        self.mobile = mobile
        self.damage = damage
        self.sigma = sigma
    
    def animate(self):
        if not self.mobile or random.random() < 0.7:
            return
        x = random.randint(self.x-1, self.x+1)
        y = random.randint(self.y-1, self.y+1)
        other = self.game.dungeon.cur_dungeon.collision_detect(x, y)
        if other == "dungeon":
            return
        self.x, self.y = x, y
    
    def on_character_touch(self, character):
        character.damage(random.gauss(self.damage, self.sigma))
    
    def render(self, scr):
        scr.chgat(self.y, self.x, 1, curses.color_pair(2))
        