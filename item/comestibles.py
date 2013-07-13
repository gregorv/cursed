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

from .itembase import Item, ItemStackable


class Comestible(Item, ItemStackable):
    symbol = "%"

    def __init__(self, game):
        Item.__init__(self, game)
        ItemStackable.__init__(self)

    def on_ingest(self, ingester):
        pass


class Apple(Comestible):
    name = "Apple"
    weight = 1
    value = 5
    symbol = "%"
    heal = 5
