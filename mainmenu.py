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


class StartMenu:
    def __init__(self, scr):
        self.scr = scr
        self.state = "main"
        self.new_game = False
        self.continue_game = False
        self.quit = False
        self.no_savegame = False

    def handle_keypress(self, code, mod):
        if self.state == "main":
            if not mod and code == "q":
                self.quit = True
            elif not mod and code == "p":
                if self.no_savegame:
                    self.new_game = True
                else:
                    self.state = "overwrite_warning"
            elif not mod and code == "c" and not self.no_savegame:
                self.continue_game = True
            else:
                return False
        elif self.state == "overwrite_warning":
            if not mod and code == "y":
                self.new_game = True
            elif not mod and code == "n":
                self.state = "main"
            else:
                return False
        else:
            return False
        return True

    def draw(self):
        self.scr.clear()
        self.scr.addstr(0, 0,
"""      ____
     / ___|   _ _ __ ___  ___  __| |
    | |  | | | | '__/ __|/ _ \/ _` |
    | |__| |_| | |  \__ \  __/ (_| |
     \____\__,_|_|  |___/\___|\__,_|""",
                        curses.A_BOLD)
        self.scr.addstr(5, 0, "    A Python based rouge-like")
        if self.state == "main":
            if not self.no_savegame:
                self.scr.addstr(8, 1,
                                "c) Continue last game")
            self.scr.addstr(9, 1,
                            "p) Start new game")
            self.scr.addstr(10, 1,
                            "h) Read Documentation")
            self.scr.addstr(11, 1,
                            "q) Quit")
        elif self.state == "overwrite_warning":
            self.scr.addstr(6, 1, "Warning!", curses.A_BOLD)
            self.scr.addstr(6, 10, "This will delete your previous savegame.")
            self.scr.addstr(7, 1, "Continue? (y/n)")
        self.scr.refresh()


