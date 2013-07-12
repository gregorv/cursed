'''
Documentation, License etc.

@package cursed
'''

import curses
import argparse
import traceback
from game import Game

def start_game(stdscr, args):
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
        
        