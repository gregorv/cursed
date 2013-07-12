
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
        
        self.map = Map(self, "1", (200, 200))
        self.map.generate()
        
        self.round = 0
        
        self.views = {}
        screen_factory = [view.Play, view.Inventory, view.PickupItems, view.MapOverview]
        for i, scr in enumerate(screen_factory):
            tmp = scr(self, self.stdscr)
            self.views[tmp.name] = tmp
            if i == 0:
                self.play_view = tmp
        self.current_view = self.play_view
        
    def set_view(self, new_active="", *args, **kwargs):
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
    
    def perform_microround(self):
        self.round += 1
        self.player.round_cooldown -= 1
        for npc in self.map.npc_list:
            if npc.npc_list == 0:
                npc.animate()
            else:
                npc.round_cooldown -= 1
        # UPDATE PARTICLES
        # DEATH CONDITION
        # REGENERATION
        

    def run(self):
        while not self.quit:
            self.map.update()
            self.current_view.draw()
            if not self.player.round_cooldown:
                curses.doupdate()
                mod = False
                code = self.stdscr.getkey()
                if code == "\x1b":
                    mod = True
                    while code == "\x1b":
                        code = self.stdscr.getkey()
                self.handle_keypress(code, mod)
            else:
                self.perform_microround()