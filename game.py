
import curses
import configparser

import view
from map import Map
from player import Player
from keymapping import Keymapping

class Game:
    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.stdscr.resize(25, 80)
        self.config = configparser.ConfigParser()
        self.config.read("cursed.cfg")
        
        self.keymap = Keymapping()
        self.keymap.import_mapping(self.config["keymap"])
        
        self.player = Player(self)
       
        self.quit = False
        
        self.map = Map(self, "1")
        
        self.views = {}
        screen_factory = [view.Play]
        for i, scr in enumerate(screen_factory):
            tmp = scr(self, self.stdscr)
            self.views[tmp.name] = tmp
            if i == 0:
                self.play_view = tmp
        self.current_view = self.play_view
        
    def set_active(self, new_active="", *args, **kwargs):
        self.current_view.on_deactivate()
        if new_active:
            self.current_view = self.views[new_active]
        else:
            self.current_view = self.play_view   
        self.current_view.on_activate(*args, **kwargs)
    
    def handle_keypress(self, code, mod):
        if self.keymap("quit", code, mod):
            self.quit = True
        else:
            return self.current_view.handle_keypress(code, mod)
        return True

    def run(self):
        while not self.quit:
            self.current_view.draw()
            curses.doupdate()
            mod = False
            code = self.stdscr.getkey()
            if code == "\x1b":
                mod = True
                while code == "\x1b":
                    code = self.stdscr.getkey()
            self.handle_keypress(code, mod)