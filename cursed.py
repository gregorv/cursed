'''
Documentation, License etc.

@package cursed
'''

import curses
import argparse
import traceback
from game import Game

def start_game(stdscr, args):
    curses.curs_set(0)
    curses.start_color()
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE);
    curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_RED);
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_YELLOW);
    curses.init_pair(4, curses.COLOR_BLACK, curses.COLOR_BLUE);
    game = Game(stdscr)
    if "u" in args:
        game.player.name = args["u"]
    if "c" in args:
        game.config.read("c")
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
    except Exception as e:
        if "t" in args:
            with open(args["t"], "w") as f:
                f.write(traceback.format_exc())
        else:
            raise
        
        