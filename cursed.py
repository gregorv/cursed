""
"""
    Cursed, a Rouge-like written in Python
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
import argparse
import traceback
from game import Game

def start_game(stdscr, args):
    curses.cbreak()
    curses.curs_set(0)
    game = Game(stdscr, extra_config=args["c"])
    if "u" in args:
        game.player.name = args["u"]
    game.run()

if __name__ == "__main__":
    parse = argparse.ArgumentParser()
    parse.add_argument("-u", default="Adventurer",
                       help="Name of the player")
    parse.add_argument("-c", default=None,
                       help="User configuration")
    parse.add_argument("-t", default=None,
                       help="Path were Python tracebacks will be stored instead of displaying them on stdout.")
    args = vars(parse.parse_args())
    try:
        curses.wrapper(start_game, args)
    except Exception, e:
        if "t" in args and args["t"]:
            with open(args["t"], "w") as f:
                f.write(traceback.format_exc())
        else:
            raise
        
        