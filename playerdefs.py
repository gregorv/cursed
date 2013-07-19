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

race_descr = {
    "troll": ("Troll", "Large, strong creatures, but not very smart"),
    "elf": ("Elf", "Smart, not very strong"),
    "human": ("Human", "Ye know, the usual"),
    "feuerviech": ("Feuerviech", "A creature from HELL"),
}

class_descr = {
    "thaumaturge": ("Thaumaturge", "?!"),
    "knight": ("Knight", "!!"),
    "archer": ("Archer", "blub"),
}

race_def = {
    "troll": {
        "char.hp": (100, 1),
        "char.mana": (0, -4),
        "char.hp_regen": (5, 0),
        "char.mana_regen": (0, -4),
        "char.strength": (10, 1),
        "char.defence": (5, 1),
        "char.magic": (0, -5),
        "char.spirit": (0, -5),
        "weapon.mace": (1, 1),
    },
    "elf": {
        "char.hp": (15, 0),
        "char.mana": (5, 1),
        "char.hp_regen": (1, 0),
        "char.mana_regen": (2, 0),
        "char.strength": (1, -1),
        "char.defence": (1, 0),
        "char.magic": (1, 1),
        "char.spirit": (1, 1),
    },
    "human": {
        "char.hp": (20, 1),
        "char.mana": (2, 0),
        "char.hp_regen": (1, 0),
        "char.mana_regen": (1, 0),
        "char.strength": (1, 0),
        "char.defence": (1, 0),
        "char.magic": (1, 0),
        "char.spirit": (1, 0),
    },
    "feuerviech": {
        "char.hp": (5, 0),
        "char.mana": (10, 1),
        "char.hp_regen": (1, 0),
        "char.mana_regen": (1, 1),
        "char.strength": (1, -1),
        "char.defence": (1, 0),
        "char.magic": (2, 0),
        "char.spirit": (2, 0),
        "elemdef.fire": (5, 3),
        "elemdef.water": (5, -3),
        "elemdef.ice": (5, -3),
        "spell.fire": (0, 3),
        "spell.firestorm": (0, 3),
    },
}

class_def = {
    "thaumaturge": {
        "char.strength": (0, -1),
        "char.magic": (2, 2),
        "char.spirit": (1, 1),
    },
    "knight": {
        "char.strength": (1, 1),
        "char.defence": (1, 1),
        "char.spirit": (0, -1),
        "char.magic": (0, -1),
        "weapon.sword": (1, 2),
    },
    "archer": {
        "char.strength": (0, -1),
        "char.magic": (2, 2),
        "char.spirit": (1, 1),
    },
}
