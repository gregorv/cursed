'''
Documentation, License etc.

@package cursed
'''

import curses
from game import Game

def start_game(stdscr):
    curses.curs_set(0)
    game = Game(stdscr)
    game.run()

if __name__ == "__main__":
    curses.wrapper(start_game)