'''
Documentation, License etc.

@package cursed
'''

import curses
from game import Game

def start_game(stdscr):
    curses.curs_set(0)
    curses.start_color()
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE);
    game = Game(stdscr)
    game.run()

if __name__ == "__main__":
    curses.wrapper(start_game)