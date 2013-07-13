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


class BaseView:
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
        if self.game.player.handle_keypress(code, mod):
            return True
        else:
            if self.game.keymap("view.play.inventory", code, mod):
                self.game.set_view("Inventory")
            if self.game.keymap("view.play.wield", code, mod):
                self.game.set_view("WieldWeapon")
            elif self.game.keymap("view.play.mapoverview", code, mod):
                self.game.set_view("MapOverview")
            else:
                return False
            return True

    def draw(self):
        self.scr.clear()
        yx = self.scr.getmaxyx()
        self.game.map.render(self.scr, (0, 0), (yx[0]-6, yx[1]//2))
        self.scr.addstr(yx[0]-2, 1, "Round {0:.1f}".format(self.game.round/10))
        self.scr.noutrefresh()
