
import curses

import gamescr

class Logger:
    def __init__(self, messagescr):
        self.scr = messagescr
        self.maxmsglen = messagescr.getmaxyx()[1]-2
        self.maxlog = messagescr.getmaxyx()[0]-3
        self.history = []
    
    def draw(self):
        self.scr.clear()
        self.scr.border()
        for i, msg in enumerate(self.history):
            self.scr.addstr(i+1, 1, msg)
        self.scr.refresh()
        
    def handle_keypress(self, code, mod):
        return False
    
    def log(self, msg):
        self.history.append(msg[:self.maxmsglen] if len(msg) > self.maxmsglen else msg)
        while(len(self.history) > self.maxlog):
            del self.history[0]

class Game:
    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.mainscr = curses.newwin(20, 59, 0, 0)
        self.infoscr = curses.newwin(20, 20, 0, 60)
        self.messagescr = curses.newwin(5, 80, 20, 0)
       
        self.quit = False
        
        self.inventory = gamescr.Inventory(self.mainscr)
        self.spells = gamescr.Spells(self.mainscr)
        self.dungeon = gamescr.Dungeon(self.mainscr)
        self.logger = Logger(self.messagescr)
        self.active_main = self.dungeon
        
        self.key_listeners = [self]
        
        
    def _draw_info(self):
        self.infoscr.clear()
        self.infoscr.border()
        self.infoscr.refresh()
        
    def handle_keypress(self, code, mod):
        if code == curses.KEY_ENTER:
            self.quit = True
        else:
            return False
        return True
        
    def draw(self):
        self._draw_info()
        self.logger.draw()
        if self.active_main:
            self.active_main.draw()

    def run(self):
        while not self.quit:
            self.draw()
            mod = False
            code = self.stdscr.getkey()
            if code == "^[":
                mod = True
                while code == "^[":
                    code = self.stdscr.getkey()
            for listener in self.key_listeners:
                if listener.handle_keypress(code, mod):
                    break
            self.logger.log("Unhandled keypress {0}".format(code))