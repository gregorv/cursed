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

import random

import particle

def trigger_action(spell, game, caster, target, position, silent=False):
    s = spell_list[spell]
    try:
        if s["spirit"] > caster.spirit:
            raise CastException("Insufficient Spirit")
        if s["mana"] > caster.mana:
            raise CastException("Insufficient Mana")
        globals()[spell](game, caster, target, position)
        caster.mana -= s["mana"]
        caster.spirit_bonus += s["mana"]*s["spirit"]*0.01
        caster.mana_bonus += s["mana"]*0.02
    except CastException as e:
        if not silent:
            game.logger.log("Cannot cast {0}: {1}".format(spell_list[spell]["name"], str(e)))
        return False
    return True

class CastException(Exception):
    pass

def firestorm(game, caster, target, position):
    for i in range(20):
        x = int(random.gauss(position[0], 1))
        y = int(random.gauss(position[1], 1))
        other = game.dungeon.cur_dungeon.collision_detect(x, y)
        if other == "dungeon":
            continue
        particle.Fire(game,
                      x, y,
                      max(5, random.gauss(8, 4)),
                      9 + caster.spirit*0.1,
                      1 + caster.spirit*0.01,
                      True)

def fire(game, caster, target, position):
    particle.Fire(game,
                  position[0], position[1],
                  max(2, random.gauss(2, 1)),
                  4+caster.spirit*0.3,
                  0.4,
                  False)

def heal(game, caster, target, pos):
    target.heal(20)

def blink(game, caster, target, pos):
    pos = game.dungeon.cur_dungeon.get_free_space()
    caster.x, caster.y = pos
    
def softdestruct(game, caster, target, pos):
    pass

def eternalhealth(game, caster, target, pos):
    caster.hp_bonus += 10

spell_list = {
    "firestorm": {
        "name": "Firestorm",
        "range": 9,
        "hotkey": "F",
        "spirit": 7,
        "mana": 200,
    },
    
    "heal": {
        "name": "Heal",
        "range": 2,
        "hotkey": "h",
        "spirit": 1,
        "mana": 10,
    },
    
    "softdestruct": {
        "name": "Soft Destruction",
        "range": 5,
        "hotkey": "d",
        "spirit": 5,
        "mana": 70,
    },
    
    "blink": {
        "name": "Blink",
        "range": None,
        "hotkey": "b",
        "spirit": 5,
        "mana": 10,
    },
    
    "fire": {
        "name": "Fire",
        "range": 4,
        "hotkey": "f",
        "spirit": 1,
        "mana": 10,
    },
    
    
    "eternalhealth": {
        "name": "Eternal Health",
        "range": None,
        "hotkey": "H",
        "spirit": 4,
        "mana": 400,
    },
}