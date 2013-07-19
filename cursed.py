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
import pickle
import os
import player
from mainmenu import StartMenu
from game import Game


class GameLoader(pickle.Unpickler):
    pass


def init(stdscr, args):
    Game.stdscr = stdscr
    curses.cbreak()
    curses.curs_set(0)
    stdscr.resize(25, 80)
    menu = StartMenu(stdscr)
    menu.no_savegame = not os.path.exists(args["s"])
    while True:
        menu.draw()
        ch = stdscr.getkey()
        menu.handle_keypress(ch, False)
        if menu.new_game:
            try:
                os.remove(args["s"])
            except OSError:
                pass
            game = Game(stdscr, extra_config=args["c"])
            if "u" in args:
                game.player_name = args["u"]
            else:
                game.player_name = "Horst"
            game.savefile = args["s"]
            game.bone_directory = args["b"]
            game.death_directory = args["d"]
            game.initialize(menu.player_race, menu.player_class)
            game.run()
            break
        elif menu.continue_game:
            with open(args["s"]) as fp:
                game = pickle.load(fp)
            os.remove(args["s"])
            game.stdscr = stdscr
            game._setup_styles()
            game.quit = False
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
    parse.add_argument("-b", default="bones/",
                       help="Bonefile directory")
    parse.add_argument("-d", default="deathlog/",
                       help="Deathlog directory")
    args = vars(parse.parse_args())
    try:
        curses.wrapper(init, args)
    except Exception, e:
        if "t" in args and args["t"]:
            with open(args["t"], "w") as f:
                f.write(traceback.format_exc())
        else:
            raise
