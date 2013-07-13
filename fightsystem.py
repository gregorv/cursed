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


def standard_physical(attacker, defender, power, skill):
    askill = attacker.effective_skills
    dskill = defender.effective_skills
    effective_str = askill["char.strength"] + askill[skill] * 2
    return ((0.1 * effective_str**2 + effective_str)
            * math.exp(-dskill["char.defence"]/20)
            * power*0.1
            )


def standard_magic(attacker, defender, power, category_skill, spell_skill):
    askill = attacker.effective_skills
    dskill = defender.effective_skills
    effective_mag = (askill["char.magic"]
                     + 1.5*askill[category_skill]
                     + 2*askill[spell_skill])
    return (effective_mag + power
            * math.exp(-dskill["char.spirit"]/20)
            * power*0.1
            )


def elemental_influence(attacker, defender, damage, element_defence):
    multiplicator = (20 - defender.effective_skills[element_defence])/20
    return damage * min(1.0, max(-1.0, multiplicator))


def status_effect(attacker, defender, damage):
    return damage

