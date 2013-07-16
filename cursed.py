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
from mainmenu import StartMenu
from game import Game


def init(stdscr, args):
    curses.cbreak()
    curses.curs_set(0)
    menu = StartMenu(stdscr)
    game = Game(stdscr, extra_config=args["c"])
    if "u" in args:
        game.player_name = args["u"]
    else:
        game.player_name = "Horst"
    game.savefile = args["s"]
    while True:
        menu.draw()
        ch = stdscr.getkey()
        menu.handle_keypress(ch, False)
        if menu.new_game:
            game.initialize()
            game.run()
            break
        elif menu.continue_game:
            game.recover_savegame()
            game.run()
            break
        if menu.quit:
            break

if __name__ == "__main__":
    parse = argparse.ArgumentParser()
    parse.add_argument("-u", default="Adventurer",
                       help="Name of the player")
    parse.add_argument("-c", default=None,
                       help="User configuration")
    parse.add_argument("-t", default=None,
                       help="Path were Python tracebacks will be stored instead of displaying them on stdout.")
    parse.add_argument("-s", default="savegame",
                       help="Path where to put the savegame")
    args = vars(parse.parse_args())
    try:
        curses.wrapper(init, args)
    except Exception, e:
        if "t" in args and args["t"]:
            with open(args["t"], "w") as f:
                f.write(traceback.format_exc())
        else:
            raise
