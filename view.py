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
import item
from map import Map


class ViewRegistry(type):
    classes = {}

    def __new__(self, name, bases, dict):
        tmp = type.__new__(self, name, bases, dict)
        if name != "BaseView":
            self.classes[name] = tmp
        return tmp


class BaseView:
    __metaclass__ = ViewRegistry

    def __init__(self, game, scr):
        self.scr = scr
        self.game = game
        self.name = self.__class__.__name__
        self.max_y, self.max_x = self.scr.getmaxyx()

    def on_activate(self):
        pass

    def on_deactivate(self):
        pass

    def handle_keypress(self, code, mod):
        if not mod and code == "\t":
            self.game.set_view()
            return True
        return False

    def draw(self):
        self.scr.clear()
        self.scr.border()
        self.scr.addstr(1, 10, self.name, curses.A_BOLD)
        self.scr.noutrefresh()


class StartMenu(BaseView):
    def __init__(self, game, scr):
        BaseView.__init__(self, game, scr)
        self.state = "main"

    def on_activate(self):
        self.state = "main"

    def handle_keypress(self, code, mod):
        if not mod and code == "q":
            self.game.quit = True
        elif not mod and code == "p":
            self.game.set_view()
            self.game.initialize_game()
        else:
            return False
        return True

    def draw(self):
        self.scr.clear()
        self.scr.addstr(0, 0,
"""      ____
     / ___|   _ _ __ ___  ___  __| |
    | |  | | | | '__/ __|/ _ \/ _` |
    | |__| |_| | |  \__ \  __/ (_| |
     \____\__,_|_|  |___/\___|\__,_|""",
                        curses.A_BOLD)
        self.scr.addstr(5, 0, "    A Python based rouge-like")
        if self.state == "main":
            self.scr.addstr(8, 1,
                            "c) Continue last game",
                            curses.color_pair(curses.COLOR_RED))
            self.scr.addstr(9, 1,
                            "p) Start new game")
            self.scr.addstr(10, 1,
                            "h) Read Documentation")
            self.scr.addstr(11, 1,
                            "q) Quit")
        elif self.state == "overwrite_warning":
            self.scr.addstr(6, 1, "Warning!", curses.A_BOLD)
            self.scr.addstr(6, 10, "This will delete your previous savegame.")
            self.scr.addstr(7, 1, "Continue? (y/n)")
        self.scr.noutrefresh()


class SkillView(BaseView):
    def __init__(self, game, scr):
        BaseView.__init__(self, game, scr)
        self.cursor_pos = (1, 1)
        self.scroll_offset = 0
        self.max_skill_view_height = self.max_y-3
        self.categories = [
            ("char.", "Character Skills"),
            ("elemdef.", "Element Defence"),
            ("weapon.", "General Weapon Skills"),
            ("magic.", "General Magic Skills"),
            ("spell.", "Spell Casting Skills"),
        ]

    def on_activate(self):
        self.cursor_pos = (0, 0)
        s = self.game.player.skills
        cat_half = len(self.categories)//2

        def num_skills_in_column(cat):
            num = 0
            for prefix, name in cat:
                num += sum(1 for k in s.get_skills()
                           if k.startswith(prefix))
            return num
        self.cursor_max_y = [num_skills_in_column(self.categories[:cat_half]),
                             num_skills_in_column(self.categories[cat_half:])]
        self.skill_cursor_data = [
            self.calc_skill_cursor_data(self.categories[:cat_half]),
            self.calc_skill_cursor_data(self.categories[cat_half:])
        ]
        self.scroll_offset = 0

    def calc_skill_cursor_data(self, categories):
        sel_y = 0
        draw_y = 0
        base_skills = self.game.player.skills
        data = []
        for prefix, name in categories:
            data.append((name, draw_y, None))
            draw_y += 1
            for skill in base_skills.get_skills():
                if not skill.startswith(prefix):
                    continue
                data.append((skill, draw_y, sel_y))
                sel_y += 1
                draw_y += 1
            draw_y += 1
        return data

    def selected_skill_position(self, cursor):
        """
        returns 0: in view
        1: below view, scroll down
        -1: above view, scroll up
        """
        for name, draw_y, sel_y in self.skill_cursor_data[cursor[1]]:
            if sel_y == cursor[0]:
                if draw_y-self.scroll_offset < 0:
                    return -1
                elif(draw_y-self.scroll_offset
                     >= self.max_skill_view_height):
                    return 1
                else:
                    return 0

    def get_selected_skill(self):
        for name, draw_y, sel_y in self.skill_cursor_data[self.cursor_pos[1]]:
            if sel_y == self.cursor_pos[0]:
                return name

    def render_column(self, y_off, x_off, categories, highlight=None):
        draw_y = y_off
        draw_y -= self.scroll_offset
        player = self.game.player
        base_skills = self.game.player.skills
        effective_skills = self.game.player.effective_skills
        sel_y = 0
        for prefix, name in categories:
            if draw_y >= y_off:
                self.scr.addstr(draw_y, x_off,
                                name,
                                curses.A_UNDERLINE)
            draw_y += 1
            for skill in base_skills.get_skills():
                if not skill.startswith(prefix):
                    continue
                if draw_y < y_off:
                    draw_y += 1
                    sel_y += 1
                    continue
                level_points = len(filter(lambda x: x == skill,
                                          player.level_skills))
                exp_percent = 100.0*level_points/len(player.level_skills)
                color = 0
                if not base_skills.can_level_skill(skill):
                    color = curses.color_pair(curses.COLOR_RED)
                self.scr.addstr(draw_y, x_off,
                                base_skills.get_skill_name(skill),
                                (curses.A_REVERSE
                                 if sel_y == highlight
                                 else curses.A_NORMAL)
                                + color)
                self.scr.addstr(draw_y, x_off+16,
                                "{0:3d}".format(base_skills[skill]),
                                color)
                self.scr.addstr(draw_y, x_off+21,
                                "{0:3d}".format(effective_skills[skill]),
                                color)
                self.scr.addstr(draw_y, x_off+25,
                                "{0:>3,.0f}%".format(exp_percent),
                                color)
                self.scr.addstr(draw_y, x_off+30,
                                "{0:4d}"
                                .format(base_skills
                                        .get_exp_to_next_level(skill)),
                                color)
                sel_y += 1
                draw_y += 1
                if draw_y >= self.max_skill_view_height + y_off:
                    break
            draw_y += 1
            if draw_y >= self.max_skill_view_height + y_off:
                break

    def render_skills(self, highlight=None):
        cat_half = len(self.categories)//2
        l_highlight = None
        r_highlight = None
        if highlight:
            if highlight[1] == 0:
                l_highlight = highlight[0]
            else:
                r_highlight = highlight[0]
        self.render_column(2, 1,
                           self.categories[:cat_half],
                           l_highlight
                           )
        self.render_column(2, self.max_x//2+1,
                           self.categories[cat_half:],
                           r_highlight
                           )
        self.scr.addstr(0, 10,
                        "Skills", curses.A_BOLD)

    def handle_keypress(self, code, mod):
        if not mod and code == "h":
            self.cursor_pos = (self.cursor_pos[0],
                               self.cursor_pos[1]-1)
        elif not mod and code == "l":
            self.cursor_pos = (self.cursor_pos[0],
                               self.cursor_pos[1]+1)
        elif not mod and code == "k":
            self.cursor_pos = (self.cursor_pos[0]-1,
                               self.cursor_pos[1])
        elif not mod and code == "j":
            self.cursor_pos = (self.cursor_pos[0]+1,
                               self.cursor_pos[1])
            #self.cursor_pos = (min(self.cursor_pos[0]+1,
                                   #self.cursor_max_y[self.cursor_pos[1]]),
                               #self.cursor_pos[1])
        elif not mod and code == "+":
            skill = self.get_selected_skill()
            base_skills = self.game.player.skills
            if base_skills.can_level_skill(skill):
                self.game.player.level_skills.append(skill)
        elif not mod and code == "-":
            skill = self.get_selected_skill()
            base_skills = self.game.player.skills
            if(base_skills.can_level_skill(skill)
               and len(self.game.player.level_skills)) > 1:
                try:
                    self.game.player.level_skills.remove(skill)
                except Exception:
                    pass
        else:
            return BaseView.handle_keypress(self, code, mod)
        self.cursor_pos = (self.cursor_pos[0],
                           max(0, min(1, self.cursor_pos[1])))
        self.cursor_pos = (max(0, min(self.cursor_max_y[self.cursor_pos[1]]-1,
                                      self.cursor_pos[0])),
                           self.cursor_pos[1])
        # minimize top distance to top -> show headlines
        self.scroll_offset = 0
        pos = self.selected_skill_position(self.cursor_pos)
        while pos != 0:
            self.scroll_offset += pos
            pos = self.selected_skill_position(self.cursor_pos)
        return True

    def draw(self):
        self.scr.clear()
        self.render_skills(self.cursor_pos)
        #for y in range(2, self.max_skill_view_height+2):
            #self.scr.addch(y, self.max_x-1, "#",
                           #curses.color_pair(curses.COLOR_WHITE
                                             #+ 8*curses.COLOR_WHITE))
        self.scr.noutrefresh()


class ItemView(BaseView):
    def __init__(self, game, scr):
        BaseView.__init__(self, game, scr)
        self.item_container = None
        self.scroll_offset = 0
        self.item_view_height = self.max_y-5

    def on_activate(self, container):
        self.item_container = container
        self.selection = []

    def render_items(self, filter_expr=None):
        if filter_expr:
            items = filter(filter_expr, self.item_container.items)
        else:
            items = self.item_container.items
        items = list(sorted(self.item_container.items,
                            key=lambda x: x.name))
        left = True
        y = self.scroll_offset+1
        for item in items[self.scroll_offset*2:
                          (self.scroll_offset+self.item_view_height)*2]:
            self.scr.addstr(y,
                            0 if left else self.max_x//2,
                            "{3}{0}{1}{2}".format(
                                item.hotkey,
                                "+" if item in self.selection else "-",
                                item.name,
                                "{0:4d}x ".format(item.count)
                                if hasattr(item, "count")
                                else "     "
                                )
                            )
            left = not left
            if left:
                y += 1

    def handle_keypress(self, code, mod):
        if self.game.keymap("view.itemview.scroll_up", code, mod):
            self.scroll_offset = max(0, self.scroll_offset - 1)
        elif self.game.keymap("view.itemview.scroll_down", code, mod):
            self.scroll_offset = min(self.scroll_offset + 1,
                                     max(0,
                                         len(self.item_container) - self.item_view_height
                                         )
                                     )
        else:
            return BaseView.handle_keypress(self, code, mod)
        return True

    def draw(self):
        self.scr.clear()
        self.render_items()
        self.scr.noutrefresh()


class Inventory(ItemView):
    def on_activate(self):
        ItemView.on_activate(self, self.game.player.inventory)

    def draw(self):
        self.scr.clear()
        self.scr.addstr(0, 10, "Inventory", curses.A_BOLD)
        self.render_items()
        self.scr.noutrefresh()


class PickupItems(ItemView):
    def handle_keypress(self, code, mod):
        if not mod:
            for i in self.item_container.items:
                if i.hotkey != code:
                    continue
                if i in self.selection:
                    self.selection.remove(i)
                else:
                    self.selection.append(i)
        if self.game.keymap("view.pickupitems.select_all", code, mod):
            if len(self.selection) == len(self.item_container.items):
                self.selection = []
            else:
                self.selection = list(self.item_container.items)
        elif self.game.keymap("view.pickupitems.pick", code, mod):
            self.game.player.inventory.add(self.selection)
            self.game.set_view()
        else:
            return ItemView.handle_keypress(self, code, mod)
        return False

    def draw(self):
        self.scr.clear()
        self.scr.addstr(0, 10, "Select Items to pick up", curses.A_BOLD)
        self.render_items()
        self.scr.addstr(self.max_y-1, 1, "^a select everything   , pick selected items", curses.A_BOLD)
        self.scr.noutrefresh()


class WieldWeapon(ItemView):
    def on_activate(self):
        ItemView.on_activate(self, self.game.player.inventory)
        #weap_cnt = len(filter(lambda x: isinstance(x, item.ItemWieldable),
                              #self.item_container.items))
        #if weap_cnt == 0:
            ## TODO log warning
            #self.game.set_view()

    def handle_keypress(self, code, mod):
        if not mod:
            for i in self.item_container.items:
                if(i.hotkey != code
                   and not isinstance(i, item.ItemWieldable)):
                    continue
                cur_wielded = self.game.player.wielded
                if cur_wielded:
                    cur_wielded.wielder = None
                    self.game.player.inventory.add(cur_wielded)
                self.game.player.wielded = i
                i.wielder = self.game.player
                self.game.set_view()
                return True
        elif self.game.keymap("view.wieldweapon.unwield", code, mod):
            cur_wielded = self.game.player.wielded
            if cur_wielded:
                cur_wielded.wielder = None
                self.game.player.inventory.add(cur_wielded)
            self.game.set_view()
            self.game.player.wielded = None
            return True
        return ItemView.handle_keypress(self, code, mod)

    def draw(self):
        self.scr.clear()
        self.scr.addstr(0, 10, "Select weapon to wield", curses.A_BOLD)
        self.render_items(lambda x: isinstance(x, item.ItemWieldable))
        self.scr.addstr(0, 10, "- unwield")
        self.scr.noutrefresh()


class MapOverview(BaseView):
    def __init__(self, game, scr):
        BaseView.__init__(self, game, scr)
        self.pos = None

    def on_activate(self):
        self.pos = self.game.player.pos

    def handle_keypress(self, code, mod):
        move = None
        if self.game.keymap("view.mapoverview.w", code, mod): move = (-1, 0)
        elif self.game.keymap("view.mapoverview.e", code, mod): move = (1, 0)
        elif self.game.keymap("view.mapoverview.n", code, mod): move = (0, -1)
        elif self.game.keymap("view.mapoverview.s", code, mod): move = (0, 1)
        elif self.game.keymap("view.mapoverview.ne", code, mod): move = (1, -1)
        elif self.game.keymap("view.mapoverview.nw", code, mod): move = (-1, -1)
        elif self.game.keymap("view.mapoverview.se", code, mod): move = (1, 1)
        elif self.game.keymap("view.mapoverview.sw", code, mod): move = (-1, 1)
        else:
            return BaseView.handle_keypress(self, code, mod)
        if move:
            self.pos = (self.pos[0]+move[0], self.pos[1]+move[1])
        return True

    def draw(self):
        self.scr.clear()
        yx = self.scr.getmaxyx()
        self.game.map.render(self.scr, (0, 0), (yx[0]-3, yx[1]), center=self.pos)
        self.scr.addstr(yx[0]-2, 1, "Round {0:.1f}".format(self.game.round/10))
        self.scr.noutrefresh()


class Play(BaseView):
    def __init__(self, game, scr):
        BaseView.__init__(self, game, scr)

    def handle_keypress(self, code, mod):
        if self.game.player.hp > 0:
            if self.game.player.handle_keypress(code, mod):
                return True

        if self.game.keymap("view.play.inventory", code, mod):
            self.game.set_view("Inventory")
        if self.game.keymap("view.play.wield", code, mod):
            self.game.set_view("WieldWeapon")
        elif self.game.keymap("view.play.mapoverview", code, mod):
            self.game.set_view("MapOverview")
        elif self.game.keymap("view.play.skills", code, mod):
            self.game.set_view("SkillView")
        else:
            return False
        return True

    def draw(self):
        self.scr.clear()
        yx = self.scr.getmaxyx()
        self.game.map.render(self.scr, (0, 0), (yx[0]-6, yx[1]-50))

        def display_bar(y, x, width, val, max, color_a, color_b):
            full = int(width*val/max)
            if full > 0:
                self.scr.addstr(y, x, "*"*full, color_a)
            if width-full > 0:
                self.scr.addstr(y, x+full, "."*(width-full), color_b)
        p = self.game.player
        display_bar(yx[0]-5, 1, 9, p.hp, p.effective_skills["char.hp"],
                    curses.color_pair(curses.COLOR_GREEN),
                    curses.color_pair(curses.COLOR_WHITE))
        display_bar(yx[0]-4, 1, 9, p.mana, p.effective_skills["char.mana"],
                    curses.color_pair(curses.COLOR_YELLOW),
                    curses.color_pair(curses.COLOR_WHITE))
        self.scr.addstr(yx[0]-5, 9,
                        "{0:->9}  Str{1:3d}  Def{2:3d}"
                        .format("{0}/{1}"
                                .format(p.hp,
                                        p.effective_skills["char.hp"]
                                        ),
                                p.effective_skills["char.strength"],
                                p.effective_skills["char.defence"],
                                ))
        self.scr.addstr(yx[0]-4, 9,
                        "{0:->9}  Mag{1:3d}  Spr{2:3d}"
                        .format("{0}/{1}"
                                .format(p.mana,
                                        p.effective_skills["char.mana"]
                                        ),
                                p.effective_skills["char.magic"],
                                p.effective_skills["char.spirit"],
                                ))
        self.scr.addstr(yx[0]-3, 1, "Level {0:3d}  Exp {1}/{2}"
                        .format(p.level,
                                p.exp_this_level(),
                                p.exp_next_level()))
        self.scr.addstr(yx[0]-2, 1, "Round {0:.1f}".format(self.game.round/10))
        self.scr.noutrefresh()
