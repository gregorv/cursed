
from __future__ import division

import curses
import ConfigParser

import view
from map import Map, RandomDungeon
from player import Player
from keymapping import Keymapping

class Game:
    def __init__(self, stdscr, extra_config=None):        
        self.config = ConfigParser.ConfigParser()
        self.config.read("cursed.cfg")
        if extra_config:
            allowed_sections = ["keymap", "style", "colorvalues"]
            cfg = ConfigParser.ConfigParser()
            cfg.read(extra_config)
            for sec in allowed_sections:
                if sec not in cfg.sections():
                    continue
                for key, val in cfg.items(sec):
                    self.config.set(sec, key, val)
        self.config = dict((sec, dict(self.config.items(sec))) for sec in self.config.sections())
        
        self.keymap = Keymapping()
        self.keymap.import_mapping(self.config["keymap"])
        
        self._setup_styles()
        self.stdscr = stdscr
        self.stdscr.resize(25, 80)
        
        self.player = Player(self)
       
        self.quit = False
        
        self.map = RandomDungeon(self, "1", (200, 200))
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
        
    def _setup_styles(self):
        # get color and attribute numbers from curses
        colors = dict((key[6:].lower(), val)
                  for key, val in curses.__dict__.items()
                  if key.startswith("COLOR_"))
        attributes = dict((key[2:].lower(), val)
                  for key, val in curses.__dict__.items()
                  if key.startswith("A_"))
        ansi_attributes = {
            "normal": 0,
            "bold": 1,
            "dim": 2,
            "underline": 3,
            "blink": 5,
            "reverse": 7,
        }
        
        self.use_color = False
        self.quick_map_draw = False
        if("use_colors" in self.config["style"]
           and self.config["style"]["use_colors"].lower()
           == "true"):
                self.use_color = True
                curses.start_color()
                for i in range(1, 64):
                    curses.init_pair(i, i%8, i//8)
        if("quick_map_draw" in self.config["style"]
           and self.config["style"]["quick_map_draw"].lower()
           == "true"):
            self.quick_map_draw = True
        self.style = {}
        self.ansi_style = {}
        for key, val in self.config["style"].items():
            if(key != "use_colors" and
               key != "quick_map_draw"):
                attr = ""
                if "," in val:
                    color, attr = map(str.strip, val.split(","))
                else:
                    color = val.strip()
                if ";" in color:
                    fg_color, bg_color = map(str.strip, color.split(";"))
                    fg_color = colors[fg_color]
                    bg_color = colors[bg_color]
                else:
                    fg_color = colors[color]
                    bg_color = colors["black"]
                if not self.use_color:
                    fg_color = 1
                    bg_color = 0
                self.style[key] = 0
                for a in attr.split():
                    self.style[key] += attributes[a]
                if self.use_color:
                    self.style[key] += curses.color_pair(fg_color + 8*bg_color)
                ansi_at = 0
                try:
                    ansi_at = attr.split()[0]
                    ansi_at = ansi_attributes[ansi_at]
                except KeyError:
                    pass
                except IndexError:
                    pass
                self.ansi_style[key] = "\033[{0};{1};{2}m".format(ansi_at,
                                                                  30+fg_color,
                                                                  40+bg_color)
                
        
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
        redraw = False
        self.round += 1
        self.player.round_cooldown -= 1
        for npc in self.map.npc_list:
            if npc.npc_list == 0:
                npc.animate()
                redraw = True
            else:
                npc.round_cooldown -= 1
        # UPDATE PARTICLES
        # DEATH CONDITION
        # REGENERATION
        return redraw

    def run(self):
        redraw = True
        while not self.quit:
            if redraw or not self.player.round_cooldown:
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
                redraw = self.handle_keypress(code, mod)
            else:
                redraw = self.perform_microround()