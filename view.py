
import curses
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

#class Inventory(BaseView):
    #def __init__(self, game, scr):
        #BaseView.__init__(self, game, scr)
        #self.mode = None
        
    #def on_activate(self, mode=None):
        #self.mode = mode
    
    #def handle_keypress(self, code, mod):
        #if not mod and code == "\t":
            #self.game.set_active()
        #elif mod and code == "w":
            #self.mode = "wield"
        #elif mod and code == "t":
            #self.mode = "throw"
        #elif mod and code == "e":
            #self.mode = "quaff"
        #elif mod and code == "d":
            #self.mode = "drop"
        #elif not mod and code == "D":
            #self.mode = "drop all"
        #elif not mod and self.mode:
            #item_names = list(self.game.player.items.keys())
            #item_names.sort()
            #for i, item in enumerate(item_names):
                #access_key = chr(ord("a")+i)
                #if access_key == code:
                    #item_obj = ItemRegistry.by_name(item)(self.game)
                    #if self.mode == "wield":
                        #self.game.player.in_hands = item_obj
                        #self.game.player_move_finished()
                        #self.game.set_active()
                    #elif self.mode == "quaff":
                        #item_obj.on_quaff(self.game.player)
                        #self.game.player.items[item] -= 1
                        #if self.game.player.items[item] == 0:
                            #del self.game.player.items[item]
                        #self.game.player_move_finished()
                        #self.game.set_active()
        #else:
            #return False
        #return True
                
    #def draw(self):
        #self.scr.clear()
        #self.scr.border()
        #self.scr.addstr(1, 10, self.name, curses.A_BOLD)
        #if not self.mode:
            #self.scr.addstr(self.scr.getmaxyx()[0]-2, 1, "^w-wield, ^t-throw, ^e-eat/quaff, ^d-drop, D-drop all")
        #else:
            #self.scr.addstr(self.scr.getmaxyx()[0]-2, 1, "Choose item to {0}".format(self.mode))
        #item_names = list(self.game.player.items.keys())
        #item_names.sort()
        #for i, item in enumerate(item_names):
            #access_key = chr(ord("a")+i)
            #amount = self.game.player.items[item]
            #self.scr.addstr(i+3, 2, "{0} - {1} {2}".format(access_key, item, "x{0}".format(amount) if amount != 1 else ""))
        #self.scr.noutrefresh()

#class Spells(BaseView):
    #def on_activate(self, mode=""):
        #self.mode = mode
    
    #def handle_keypress(self, code, mod):
        #if not mod and self.mode == "cast":
            #for s in self.game.player.spells:
                #if spell.spell_list[s]["hotkey"] == code:
                    #self.game.set_active("SpellCast", s)
                    #return True
            #return BaseView.handle_keypress(self, code, mod)
        #elif mod and code == "x":
            #self.mode = "cast"
        #else:
            #return BaseView.handle_keypress(self, code, mod)
        #return True
    
    #def draw(self):
        #self.scr.clear()
        #self.scr.border()
        #self.scr.addstr(1, 10, "Spells & Magic", curses.A_BOLD)
        #if self.mode == "cast":
            #self.scr.addstr(self.max_y-2, 1, "Select spell to cast", curses.A_BOLD)
        #else:
            #self.scr.addstr(self.max_y-2, 1, "^x-Cast Spell", curses.A_BOLD)
        #for i, s in enumerate(self.game.player.spells):
            #self.scr.addstr(3+i, 1, "{hotkey} - {name}, Range {range}, MNA {mana}, SPR {spirit}".format(**spell.spell_list[s]))
        #self.scr.noutrefresh()
        
#class PickTarget(BaseView):
    #def __init__(self, game, scr):
        #BaseView.__init__(self, game, scr)
        #self.cursor_position = 0, 0
        
    #def do_move(self, x, y):
        #return True
    
    #def on_activate(self):
        #self.cursor_position = self.game.player.x, self.game.player.y
    
    #def handle_keypress(self, code, mod):
        #move_cursor = 0, 0
        #if mod:
            #return False
        #if code == "\t":
            #self.game.set_active()
        #elif code in ("w", "j"): move_cursor = 0, -1
        #elif code in ("a", "h"): move_cursor = -1, 0
        #elif code in ("s", "k"): move_cursor = 0, 1
        #elif code in ("d", "l"): move_cursor = 1, 0
        #elif code in ("q", "y"): move_cursor = -1, -1
        #elif code in ("e", "u"): move_cursor = 1, -1
        #elif code in ("y", "b"): move_cursor = -1, 1
        #elif code in ("c", "n"): move_cursor = 1, 1
        #else:
            #return False
        
        #if move_cursor != (0, 0):
            #move_cursor = (move_cursor[0] + self.cursor_position[0],
                           #move_cursor[1] + self.cursor_position[1])
            #x, y = move_cursor
            #if(x < self.max_x-1 and y < self.max_y-1
               #and x > 0 and y > 0):
                #if self.do_move(*move_cursor):
                    #self.cursor_position = move_cursor
        
        #return True
    
    #def draw(self):
        #self.scr.clear()
        #self.game.dungeon.cur_dungeon.render(self.scr)
        #self.scr.addch(self.game.player.y,
                       #self.game.player.x,
                       #"@")
        #self.scr.chgat(self.cursor_position[1],
                       #self.cursor_position[0],
                       #1,
                       #curses.color_pair(1))
        #self.scr.noutrefresh()

#class AnalyzeEnemy(PickTarget):
    #def on_activate(self):
        #PickTarget.on_activate(self)
        #self.game.info_override = self.info_draw
    
    #def on_deactivate(self):
        #self.game.info_override = None
        
    #def info_draw(self, scr):
        #scr.clear()
        #scr.border()
        #sel_npc = None
        #for npc in self.game.dungeon.cur_dungeon.npc_list:
            #if (npc.x, npc.y) == self.cursor_position:
                #sel_npc = npc
                #break
        #if sel_npc:
            #scr.addstr(3, 1, sel_npc.name)
            #scr.addstr(4, 1, "LVL {n.level}".format(n=sel_npc))
            #scr.addstr(5, 1, "HP  {n.hp}/{n.max_hp}".format(n=sel_npc))
            #scr.addstr(6, 1, "EXP on kill {0}".format(sel_npc.exp_loot()))
        #else:
            #scr.addstr(2, 1, "No NPC found")
        #scr.addstr(1, 2, "NPC Information", curses.A_BOLD)
        
        #scr.noutrefresh()

#class SpellCast(PickTarget):
    #def do_move(self, x, y):
        #if not self.selection_range:
            #return True
        #dist = (self.game.player.x - x)**2
        #dist += (self.game.player.y - y)**2
        #return self.selection_range**2 > dist
    
    #def on_activate(self, spell_name):
        #PickTarget.on_activate(self)
        #self.spell_name = spell_name
        #self.spell = spell.spell_list[spell_name]
        #if self.spell["range"]:
            #self.selection_range = self.spell["range"]
        #else:
            #spell.trigger_action(self.spell_name,
                                 #self.game,
                                 #self.game.player,
                                 #self.game.player,
                                 #(self.game.player.x,
                                  #self.game.player.y))
            #self.game.set_active()
        
    #def handle_keypress(self, code, mod):
        #if not mod and code == "x":
            #other = self.game.dungeon.cur_dungeon.collision_detect(*self.cursor_position)
            #if other in ("dungeon", "<", ">"):
                #other = None
            #if spell.trigger_action(self.spell_name,
                                 #self.game,
                                 #self.game.player,
                                 #other,
                                 #self.cursor_position):
                #self.game.player_move_finished()
            #self.game.set_active()
            #return True
        #else:
            #return PickTarget.handle_keypress(self, code, mod)
            
#class BaseMapView(BaseView):
    #def __init__(self, game, scr):

class ItemView(BaseView):
    def __init__(self, game, scr):
        BaseView.__init__(self, game, scr)
        self.item_container = None
        self.scroll_offset = 0
        self.item_view_height = self.max_y-5
    
    def on_activate(self, container):
        self.item_container = container
        self.selection = []
        
    def render_items(self):
        items = list(sorted(self.item_container.items,
                            key= lambda x: x.name))
        left = True
        y = self.scroll_offset+1
        for item in items[self.scroll_offset*2
                          :(self.scroll_offset+self.item_view_height)*2]:
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

class Play(BaseView):
    def __init__(self, game, scr):
        BaseView.__init__(self, game, scr)
    
    def handle_keypress(self, code, mod):
        if self.game.player.handle_keypress(code, mod):
            return True
        else:
            if self.game.keymap("view.play.inventory", code, mod):
                self.game.set_view("Inventory", self.game.player.inventory)
            else:
                return False
            return True
        
    def draw(self):
        self.scr.clear()
        yx = self.scr.getmaxyx()
        self.game.map.render(self.scr, (0, 0), (yx[0]-3, yx[1]))
        self.scr.addstr(yx[0]-2, 1, "Round {0:.1f}".format(self.game.round/10))
        self.scr.noutrefresh()
