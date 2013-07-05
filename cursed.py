'''
Documentation, License etc.

@package cursed
'''

import curses
import time

class Logger:
    def __init__(self, messagescr):
        self.scr = messagescr
        self.maxmsglen = messagescr.getmaxyx()[1]-2
        self.maxlog = messagescr.getmaxyx()[0]-3
        self.history = []
    
    def draw(self):
        self.scr.border()
        for i, msg in enumerate(self.history):
            self.scr.addstr(i+1, 1, msg)
        self.scr.refresh()
        
    def handle_keypress(self, code):
        return False
    
    def log(self, msg):
        self.history.append(msg[:self.maxmsglen] if len(msg) > self.maxmsglen else msg)
        if len(self.history) > self.maxlog:
            self.history = self.history[-1:-self.maxlog]
            
class Inventory:
    def __init__(self, scr):
        self.scr = scr
        
    def handle_keypress(self, code):
        return False
        
    def draw(self):
        self.scr.border()
        self.scr.addstr(1, 10, "Inventory", curses.A_BOLD)
        self.scr.refresh()

class Spells:
    def __init__(self, scr):
        self.scr = scr
        
    def handle_keypress(self, code):
        return False
        
    def draw(self):
        self.scr.border()
        self.scr.addstr(1, 10, "Spells & Magic", curses.A_BOLD)
        self.scr.refresh()

class Fightdisplay:
    def __init__(self, scr):
        self.scr = scr
        
    def handle_keypress(self, code):
        return False
        
    def draw(self):
        self.scr.refresh()
        
class Game:
    def __init__(self):
        self.mainscr = curses.newwin(20, 59, 0, 0)
        self.infoscr = curses.newwin(20, 20, 0, 60)
        self.messagescr = curses.newwin(5, 80, 20, 0)
        
        self.inventory = Inventory(self.mainscr)
        self.spells = Spells(self.mainscr)
        self.fightdisplay = Fightdisplay(self.mainscr)
        self.logger = Logger(self.messagescr)
        
        self.active_main =  self.fightdisplay
        
    def _draw_info(self):
        self.infoscr.border()
        self.infoscr.refresh()
        
    def handle_keypress(self, code):
        return False
        
    def draw(self):
        self._draw_info()
        self.logger.draw()
        if self.active_main:
            self.active_main.draw()

def main(stdscr):
    curses.start_color()
    curses.curs_set(0)
    mainscr = curses.newwin(20, 59, 0, 0)
    infoscr = curses.newwin(20, 20, 0, 60)
    messagescr = curses.newwin(5, 80, 20, 0)
    
    infoscr.border()
    infoscr.refresh()
    
    inventory = Inventory(mainscr)
    fightdisplay = Fightdisplay(mainscr)
    
    logger = Logger(messagescr)
    logger.log("Hello curses!")
    logger.draw()
    
    i = 0
    while True:
        fightdisplay.draw()
        time.sleep(2)
        inventory.draw()
        time.sleep(2)
        

if __name__ == "__main__":
    curses.wrapper(main)