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
        # internal name: default, base_exp, verbose_name, descr., cond
        "char.hp": (25, None, "Health", "Maximum health points", lambda s: True),
        "char.mana": (50, None, "Mana", "Maximum mana", lambda s: True),
        "char.hp_regen": (250, None, "HP Regen", "HP Regeneration rate", lambda s: True),
        "char.mana_regen": (250, None, "Mana Regen", "Mana Regeneration rate", lambda s: True),
        "char.strength": (500, None, "Strength", "Physical attack strength", lambda s: True),
        "char.defence": (1000, None, "Defence", "Defence against physical attacks", lambda s: True),
        "char.magic": (500, None, "Magic", "Magical strength", lambda s: True),
        "char.spirit": (1000, None, "Spirit", "Defence against magical attacks", lambda s: True),
        "weapon.sword": (500, None, "Swords and Daggers", "Sword attack damage", lambda s: True),
        "weapon.mace": (500, None, "Mace and Clubs", "Mace and Club fighting skill", lambda s: True),
        "weapon.staff": (500, None, "Staffs", "Staff fighting skill", lambda s: True),
        "weapon.bow": (500, None, "Bows and Arrows", "Bow fighting skill", lambda s: True),
        "magic.elemental": (500, None, "Elemental Magic", "Elemental magical strength", lambda s: True),
        "magic.neutral": (500, None, "Neutral Magic", "Strength of non-elemental magic", lambda s: True),
        "magic.healing": (500, None, "Healing Magic", "Non-elemental magic strength", lambda s: True),
        "magic.status": (500, None, "Status Magic", "State changing magic", lambda s: True),
        "elemdef.fire": (750, 40, "Fire", "Defence against elementary damage", lambda s: True),
        "elemdef.water": (750, 40, "Water", "Defence against elementary damage", lambda s: True),
        "elemdef.ice": (750, 40, "Ice", "Defence against elementary damage", lambda s: True),
        "elemdef.wind": (750, 40, "Wind", "Defence against elementary damage", lambda s: True),
        "elemdef.earth": (750, 40, "Earth", "Defence against elementary damage", lambda s: True),
        "spell.fire": (750, None, "Fire", "A simple fire spell", lambda s: s["char.magic"] >= 2),
        "spell.water": (750, None, "Water", "A basic fire spell", lambda s: s["char.magic"] >= 2),
        "spell.ice": (750, None, "Ice", "A basic fire spell", lambda s: s["char.magic"] >= 2),
        "spell.wind": (750, None, "Wind", "A basic fire spell", lambda s: s["char.magic"] >= 2),
        "spell.tornado": (1250, None, "Tornado", "A basic fire spell", lambda s: s["char.magic"] >= 3),
        "spell.firestorm": (1750, None, "Firestorm", "A basic fire spell", lambda s: s["char.magic"] >= 4),
        "spell.quake": (1750, None, "Earthquake", "A basic fire spell", lambda s: s["char.magic"] >= 4),
        "spell.heal": (250, None, "Heal", "A basic fire spell", lambda s: s["char.magic"] >= 1),
        "spell.invincibility": (2250, None, "Invincibility", "A basic fire spell", lambda s: s["char.magic"] >= 5),
        "spell.haste": (1250, None, "Haste", "A basic fire spell", lambda s: s["char.magic"] >= 3),
        "spell.slow": (1250, None, "Slow", "A basic fire spell", lambda s: s["char.magic"] >= 3),
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
        self.base_level = dict((s, 0)
                               for s, d in SkillSet.skill_def.items())
        self.skill_usage = dict((s, 0)
                                for s in SkillSet.skill_def.keys())
        self.exp_list = dict((s, 0)
                             for s in SkillSet.skill_def.keys())
        self.aptitude = dict((s, 0)
                             for s in SkillSet.skill_def.keys())

    def __getitem__(self, skill):
        return (self.base_level[skill]
                + self.exp_list[skill] // self.get_exp_per_level(skill))

    def __setitem__(self, skill, lvl):
        self.base_level[skill] = lvl

    def get_skills(self):
        return list(sorted(self.base_level.keys(),
                    key=lambda x: self.get_exp_per_level(x)))

    def get_skill_name(self, skill):
        return SkillSet.skill_def[skill][2]

    def get_skill_desciption(self, skill):
        return SkillSet.skill_def[skill][3]

    def get_exp(self, skill):
        return self.exp_list[skill]

    def get_exp_per_level(self, skill):
        return int(SkillSet.skill_def[skill][0]
                   * (5 - self.aptitude[skill]) / 5)

    def get_exp_to_next_level(self, skill):
        return self.get_exp_per_level(skill) - \
            self.exp_list[skill] % self.get_exp_per_level(skill)

    def get_aptitude(self, skill):
        return self.aptitude[skill]

    def add_exp(self, skill, exp):
        self.exp_list[skill] += exp

    def replace_levels(self, other_set):
        for skill, level in other_set.base_level.items():
            self.base_level[skill] = level
            self.exp_list[skill] = other_set.get_exp(skill)

    def use(self, skill):
        self.skill_usage[skill] += 1

    def set_base_level(self, skill, level):
        self.base_level[skill] = level

    def can_level_skill(self, skill):
        condition = SkillSet.skill_def[skill][4]
        return condition(self) if condition else True

    def add_base_definition(self, defs):
        for skill, (level, apt) in defs.items():
            self.base_level[skill] += level
            self.aptitude[skill] += apt

class Entity(object):
    """
    Things knowing the concept of life and the space-time.
    """
    def __init__(self, game):
        self.game = game
        self.pos = (1, 1)
        self.symbol = " "
        self.round_cooldown = 0
        self.effective_skills = SkillSet()
        self.hp = self.effective_skills["char.hp"]
        self.mana = self.effective_skills["char.mana"]
        self.symbol = ""
        self.style = 0
        self.level = 1

    def pre_round(self):
        pass

    def animate(self):
        pass

    def post_round(self):
        pass

    def regenerate(self):
        if self.hp > 0:
            self.hp = min(self.effective_skills["char.hp"],
                          self.hp + self.effective_skills["char.hp_regen"])
            self.mana = min(self.effective_skills["char.mana"],
                            self.hp + self.effective_skills["char.mana_regen"])

    def set_round_cooldown(self, time_required):
        self.round_cooldown = int(time_required)

    def attack(self, attacker, physical_power, magic_power):

        return self.hp <= 0

