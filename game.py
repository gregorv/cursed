""
from __future__ import division
"""
    This file is part of Cursed
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
import ConfigParser

from view import ViewRegistry
from map import Map, RandomDungeon
from player import Player
from keymapping import Keymapping
from item import ItemRegistry
import pickle


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
        self.config = dict((sec, dict(self.config.items(sec)))
                           for sec in self.config.sections())

        self.keymap = Keymapping()
        self.keymap.import_mapping(self.config["keymap"])

        self._setup_styles()
        self.stdscr = stdscr

        self.map = None
        self.player = None

        self.quit = False
        self.round = 0

        self._create_views()

    def _create_views(self):
        self.views = {}
        for name, View in ViewRegistry.classes.items():
            tmp = View(self, self.stdscr)
            self.views[name] = tmp
            if name == "Play":
                self.play_view = tmp
                self.current_view = tmp

    def initialize(self):
        self.player = Player(self)
        sword = ItemRegistry.create(self, "WoodenSword")
        self.player.inventory.add(sword)
        self.map = RandomDungeon(self, "1", (200, 200))
        self.map.generate()
        self.player.pos = self.map.get_free_space()

        self.player.skills.set_base_level("char.hp_regen", 3)
        self.player.skills.set_base_level("char.mana_regen", 1)

        self.current_view.on_activate()

    def recover_savegame(self):
        with open(self.savefile) as fp:
            data = json.load(fp)

    def save_game(self):
        with open(self.savefile, "w") as fp:
            pickle.dump(self, fp, 2)

    def __getstate__(self):
        blacklist = ["use_color", "views", "current_view",
                     "quick_map_draw", "style", "ansi_style", "play_view",
                     "stdscr"]
        state = dict((k, v) for k, v in self.__dict__.items()
                     if k not in blacklist)
        state["current_view"] = self.current_view.__class__.__name__
        return state

    def __setstate__(self, state):
        self.stdscr = Game.stdscr
        assert self.stdscr is not None
        self._create_views()
        self.__dict__.update(state)
        self.current_view = self.views[self.current_view]

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
                    curses.init_pair(i, i % 8, i//8)
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

    def save_bonefile(self):
        pass

    def save_deathlog(self):
        pass

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
        self.current_view.update()
        self.player.pre_round()
        for npc in self.map.npc_list:
            npc.pre_round()
        redraw = False
        self.round += 1
        self.player.round_cooldown = max(self.player.round_cooldown-1, 0)
        for npc in self.map.npc_list:
            if npc.round_cooldown == 0:
                npc.animate()
                redraw = True
            else:
                npc.round_cooldown -= 1
        # UPDATE PARTICLES
        # DEATH CONDITION
        if self.player.hp <= 0:
            self.save_bonefile()
            self.save_deathlog()
            return
        self.map.npc_list = list(filter(
            lambda npc: npc.hp > 0,
            self.map.npc_list
        ))
        self.player.post_round()
        for npc in self.map.npc_list:
            npc.post_round()
        return redraw

    def perform_round(self):
        self.current_view.round_update()
        self.player.regenerate()
        for npc in self.map.npc_list:
            npc.regenerate()

    def run(self):
        redraw = True
        self.current_view.update()
        self.current_view.round_update()
        try:
            while not self.quit:
                if redraw or not self.player.round_cooldown:
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
                    if self.round % 10 == 0:
                        self.perform_round()
        except KeyboardInterrupt:
            pass
        if self.player.hp > 0:
            self.save_game()
