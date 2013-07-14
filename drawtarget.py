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

class DrawTarget:
    """
    A simplified, abstracted curses window that better suits the needs
    for map rendering.
    
    For map-rendering it would be useful if there was a way to specify
    the draw style (attributes, color etc) per character. The DrawTarget
    is basicaly a two-dimensional array with each entry representing a
    character and its draw style.
    
    This array can then be converted to a list of strings, that each
    have only a single draw style and, if drawn in order, build the
    complete screen.
    """
    def __init__(self, size):
        self.size = size
        self.clear()

    def clear(self):
        self.data = [[(0, "")
                      for i in range(self.size[1])]
                     for i in range(self.size[0])]

    def addstr(self, y, x, string, attributes=0):
        """
        Curses compatible window.addstr method
        """
        line = self.data[y]
        for i, s in enumerate(string):
            line[x+i] = (attributes, s)

    def addch(self, y, x, ch, attrib=0):
        """
        Curses compatible window.addch method
        """
        self.data[y][x] = (attrib, ch)

    def chgat(self, y, x, n, attrib=None):
        """
        Curses compatible window.chgat method
        """
        if attrib is None:
            attrib = n
            n = self.size[0]-x
        for x_at in range(x, x+n):
            old_attr, ch = self.data[y][x]
            self.data[y][x] = (attrib, ch)

    def draw(self, scr, y=0, x=0):
        """
        Display the DrawTarget in a curses screen
        """
        for yidx, row in enumerate(self.data):
            cur_attr = row[0][0]
            cur_string = ""
            start_x = 0
            for xidx, (attr, ch) in enumerate(row):
                if attr == cur_attr:
                    continue
                scr.addstr(y+yidx, x+start_x,
                           "".join(ch for a, ch in row[start_x:xidx]),
                           cur_attr)
                cur_attr = attr
                start_x = xidx
                cur_string = ch
            scr.addstr(y+yidx, x+start_x,
                        "".join(ch for a, ch in row[start_x:]),
                        cur_attr)