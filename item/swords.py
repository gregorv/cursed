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

from .itembase import Item, ItemWieldable
import fightsystem


class Sword(Item, ItemWieldable):
    def __init__(self, game):
        Item.__init__(self, game)
        ItemWieldable.__init__(self)
        self.attack_power = 5

    def get_attack_struct(self):
        sword_lvl = self.wielder.skill_set["sword"]
        strength = self.wielder.skill_set["strength"]
        return {
            "damage": sword_lvl*5 + strength,
            "status": {},
            "elemental": {}
        }

    def on_wield_attack(self, target):
        self.wielder.effective_skills.use("weapon.sword")
        dmg = fightsystem.standard_physical(self.wielder,
                                            target,
                                            self.attack_power,
                                            "weapon.sword")
        dmg = fightsystem.status_effect(self, target, dmg)
        target.hp = int(max(0, target.hp - dmg))
        return target.hp == 0


class WoodenSword(Sword):
    weight = 4
    value = 10
    symbol = "t"
    name = "Wooden Sword"

    def __init__(self, game):
        Sword.__init__(self, game)
        self.attack_power = 10
