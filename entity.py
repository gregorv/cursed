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


class SkillCollector:
    def __new__(self, name, bases, cls_dict):
        if "skill_def" in cls_dict:
            SkillSet.add_skill_def(cls_dict["skill_def"])
            del cls_dict["skill_def"]
        return type(name, bases, cls_dict)


class SkillSet:
    skill_def = {
        # internal name, default, base_exp, verbose_name, descr., cond
        "char.hp": (30, 25, None, "Health", "Maximum health points", lambda s: True),
        "char.mana": (1, 50, None, "Mana", "Maximum mana", lambda s: True),
        "char.hp_regen": (1, 10, None, "HP Regen", "HP Regeneration rate", lambda s: True),
        "char.mana_regen": (1, 10, None, "Mana Regen", "Mana Regeneration rate", lambda s: True),
        "char.strength": (1, 500, None, "Strength", "Physical attack strength", lambda s: True),
        "char.defence": (1, 1000, None, "Defence", "Defence against physical attacks", lambda s: True),
        "char.magic": (1, 3000, None, "Magic", "Magical strength", lambda s: True),
        "char.spirit": (1, 1000, None, "Spirit", "Defence against magical attacks", lambda s: True),
        "weapon.sword": (0, 1000, None, "Swords and Daggers", "Sword attack damage", lambda s: True),
        "weapon.mace": (0, 1000, None, "Mace and Clubs", "Mace and Club fighting skill", lambda s: True),
        "weapon.staff": (0, 1000, None, "Staffs", "Staff fighting skill", lambda s: True),
        "weapon.bow": (0, 1000, None, "Bows and Arrows", "Bow fighting skill", lambda s: True),
        "magic.elemental": (0, 1000, None, "Elemental Magic", "Elemental magical strength", lambda s: True),
        "magic.neutral": (0, 1000, None, "Neutral Magic", "Strength of non-elemental magic", lambda s: True),
        "magic.healing": (0, 1000, None, "Healing Magic", "Non-elemental magic strength", lambda s: True),
        "magic.status": (0, 1000, None, "Status Magic", "State changing magic", lambda s: True),
        "elemdef.fire": (0, 1000, 40, "Fire", "Defence against elementary damage", lambda s: True),
        "elemdef.water": (0, 1000, 40, "Fire", "Defence against elementary damage", lambda s: True),
        "elemdef.ice": (0, 1000, 40, "Fire", "Defence against elementary damage", lambda s: True),
        "elemdef.wind": (0, 1000, 40, "Fire", "Defence against elementary damage", lambda s: True),
        "elemdef.earth": (0, 1000, 40, "Fire", "Defence against elementary damage", lambda s: True),
        "spell.fire": (0, 1250, None, "Fire", "A simple fire spell", lambda s: s["char.magic"] >= 2),
        "spell.water": (0, 1250, None, "Water", "A basic fire spell", lambda s: s["char.magic"] >= 2),
        "spell.ice": (0, 1250, None, "Ice", "A basic fire spell", lambda s: s["char.magic"] >= 2),
        "spell.wind": (0, 1250, None, "Wind", "A basic fire spell", lambda s: s["char.magic"] >= 2),
        "spell.tornado": (0, 1750, None, "Tornado", "A basic fire spell", lambda s: s["char.magic"] >= 3),
        "spell.firestorm": (0, 2250, None, "Firestorm", "A basic fire spell", lambda s: s["char.magic"] >= 4),
        "spell.quake": (0, 2250, None, "Earthquake", "A basic fire spell", lambda s: s["char.magic"] >= 4),
        "spell.heal": (0, 1000, None, "Heal", "A basic fire spell", lambda s: s["char.magic"] >= 1),
        "spell.invincibility": (0, 2750, None, "Invincibility", "A basic fire spell", lambda s: s["char.magic"] >= 5),
        "spell.haste": (0, 1750, None, "Haste", "A basic fire spell", lambda s: s["char.magic"] >= 3),
        "spell.slow": (0, 1750, None, "Slow", "A basic fire spell", lambda s: s["char.magic"] >= 3),
    }

    @classmethod
    def add_skill_def(cls, skills, default=None, max_level=None, base_exp=None,
                      verbose_name=None, description=None, condition=None):
        if(default is None and verbose_name is None and description is None
           and condition is None and base_exp is None and max_level is None):
            cls.skill_def[skills] = (default, max_level, verbose_name,
                                     base_exp, description, condition)
        else:
            cls.skill_def.update(skills)

    def __init__(self):
        # initialize with default values
        self.skills = dict((s, d[0])
                           for s, d in SkillSet.skill_def.items())

    def __index__(self, skill):
        return self.skills[skill]


class Entity:
    """
    Things knowing the concept of life and the space-time.
    """
    def __init__(self, game):
        self.game = game
        self.hp = 100
        self.pos = (1, 1)
        self.symbol = " "
        self.round_cooldown = 0
        self.effective_skills = SkillSet()

    def set_round_cooldown(self, time_required):
        self.round_cooldown = int(time_required)

    def attack(self, attacker, physical_power, magic_power):

        return self.hp <= 0

