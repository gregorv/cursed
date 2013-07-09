
import curses
import dungeon
from registry import ItemRegistry

class BaseScreen:
    
    def __init__(self, game, scr):
        self.scr = scr
        self.game = game
        self.name = self.__class__.__name__
        
    def on_activate(self):
        pass
    
    def on_deactivate(self):
        pass

    def handle_keypress(self, code, mod):
        if not mod and code == "\t":
            self.game.set_active()
            return True
        return False
        
    def draw(self):
        self.scr.clear()
        self.scr.border()
        self.scr.addstr(1, 10, self.name, curses.A_BOLD)
        self.scr.noutrefresh()

class Inventory(BaseScreen):
    def __init__(self, game, scr):
        BaseScreen.__init__(self, game, scr)
        self.mode = None
        
    def on_deactivate(self):
        self.mode = None
    
    def handle_keypress(self, code, mod):
        if not mod and code == "\t":
            self.game.set_active()
        elif mod and code == "w":
            self.mode = "wield"
        elif mod and code == "t":
            self.mode = "throw"
        elif mod and code == "e":
            self.mode = "quaff"
        elif mod and code == "d":
            self.mode = "drop"
        elif not mod and code == "D":
            self.mode = "drop all"
        elif not mod and self.mode:
            item_names = list(self.game.player.items.keys())
            item_names.sort()
            for i, item in enumerate(item_names):
                access_key = chr(ord("a")+i)
                if access_key == code:
                    item_obj = ItemRegistry.by_name(item)(self.game)
                    if self.mode == "wield":
                        self.game.player.in_hands = item_obj
                        self.game.player_move_finished()
                        self.game.set_active()
                    elif self.mode == "quaff":
                        item_obj.on_quaff(self.game.player)
                        self.game.player.items[item] -= 1
                        if self.game.player.items[item] == 0:
                            del self.game.player.items[item]
                        self.game.player_move_finished()
                        self.game.set_active()
        else:
            return False
        return True
                
    def draw(self):
        self.scr.clear()
        self.scr.border()
        self.scr.addstr(1, 10, self.name, curses.A_BOLD)
        if not self.mode:
            self.scr.addstr(self.scr.getmaxyx()[0]-2, 1, "^w-wield, ^t-throw, ^e-eat/quaff, ^d-drop, D-drop all")
        else:
            self.scr.addstr(self.scr.getmaxyx()[0]-2, 1, "Choose item to {0}".format(self.mode))
        item_names = list(self.game.player.items.keys())
        item_names.sort()
        for i, item in enumerate(item_names):
            access_key = chr(ord("a")+i)
            amount = self.game.player.items[item]
            self.scr.addstr(i+3, 2, "{0} - {1} {2}".format(access_key, item, "x{0}".format(amount) if amount != 1 else ""))
        self.scr.noutrefresh()

class Spells(BaseScreen):
    
    def draw(self):
        self.scr.clear()
        self.scr.border()
        self.scr.addstr(1, 10, "Spells & Magic", curses.A_BOLD)
        self.scr.noutrefresh()
        
class PickTarget(BaseScreen):
    def __init__(self, game, scr):
        BaseScreen.__init__(self, game, scr)
        self.cursor_position = 0, 0
        
    def do_move(self, x, y):
        return True
    
    def on_activate(self):
        self.cursor_position = self.game.player.x, self.game.player.y
    
    def handle_keypress(self, code, mod):
        move_cursor = 0, 0
        if mod:
            return False
        if code == "\t":
            self.game.set_active()
        elif code == "w": move_cursor = 0, -1
        elif code == "a": move_cursor = -1, 0
        elif code == "s": move_cursor = 0, 1
        elif code == "d": move_cursor = 1, 0
        elif code == "q": move_cursor = -1, -1
        elif code == "e": move_cursor = 1, -1
        elif code == "y": move_cursor = -1, 1
        elif code == "c": move_cursor = 1, 1
        else:
            return False
        
        if move_cursor != (0, 0):
            move_cursor = (move_cursor[0] + self.cursor_position[0],
                           move_cursor[1] + self.cursor_position[1])
            if self.do_move(*move_cursor):
                self.cursor_position = move_cursor
        
        return True
    
    def draw(self):
        self.scr.clear()
        self.game.dungeon.cur_dungeon.render(self.scr)
        self.scr.addch(self.game.player.y,
                       self.game.player.x,
                       "@")
        self.scr.chgat(self.cursor_position[1],
                       self.cursor_position[0],
                       1,
                       curses.color_pair(1))
        self.scr.noutrefresh()

class AnalyzeEnemy(PickTarget):
    pass
    
class Dungeon(BaseScreen):
    def __init__(self, game, scr):
        BaseScreen.__init__(self, game, scr)
        self.level = 1
        max_y, max_x = self.scr.getmaxyx()
        self.dungeons = {1: dungeon.Dungeon(self.game, 1, max_x, max_y)}
        self.cur_dungeon = self.dungeons[self.level]
        self.cur_dungeon.generate()
        self.cur_dungeon.on_enter()
        
    def next_dungeon(self):
        self.dungeons[self.level].on_exit()
        self.level += 1
        if self.level not in self.dungeons:
            max_y, max_x = self.scr.getmaxyx()
            self.dungeons[self.level] = dungeon.Dungeon(self.game, self.level, max_x, max_y)
            self.dungeons[self.level].generate()
        self.dungeons[self.level].on_enter()
        self.cur_dungeon = self.dungeons[self.level]
        self.game.player.x, self.game.player.y = self.cur_dungeon.pos_stairs_in
        
    def prev_dungeon(self):
        if self.level == 1:
            return
        self.dungeons[self.level].on_exit()
        self.level -= 1
        self.dungeons[self.level].on_enter()
        self.cur_dungeon = self.dungeons[self.level]
        self.game.player.x, self.game.player.y = self.cur_dungeon.pos_stairs_out
    
    def handle_keypress(self, code, mod):
        move_player = 0, 0
        if mod:
            if code == "q": self.game.quit = True
            else:
                return BaseScreen.handle_keypress(self, code, mod)
        else:
            if code == "i": self.game.set_active("Inventory")
            elif code == "x": self.game.set_active("Spells")
            elif code == "v": self.game.set_active("AnalyzeEnemy")
            elif code == "b":
                self.game.player.exp += 1
                self.game.player.apply_exp()
            elif code == "n":
                self.game.player.exp += 10
                self.game.player.apply_exp()
            elif code == "m":
                self.game.player.exp += 100
                self.game.player.apply_exp()
            elif code == "w": move_player = 0, -1
            elif code == "a": move_player = -1, 0
            elif code == "s": move_player = 0, 1
            elif code == "d": move_player = 1, 0
            elif code == "q": move_player = -1, -1
            elif code == "e": move_player = 1, -1
            elif code == "y": move_player = -1, 1
            elif code == "c": move_player = 1, 1
            elif code == ".": self.game.player_move_finished()
            elif code == "<" and self.level > 1:
                if((self.game.player.x, self.game.player.y)
                   == self.cur_dungeon.pos_stairs_in):
                    self.prev_dungeon()
            elif code == ">":
                if((self.game.player.x, self.game.player.y)
                   == self.cur_dungeon.pos_stairs_out):
                    self.next_dungeon()
            elif code == "r":
                items = self.cur_dungeon.pop_items(self.game.player.x, self.game.player.y)
                if items:
                    name_set = set(items)
                    logmsg = "Picked up a "+"and a".join(name_set)
                    self.game.logger.log(logmsg)
                    self.game.player.add_items(items)
                    self.game.player_move_finished()
            else:
                return BaseScreen.handle_keypress(self, code, mod)
        if move_player != (0, 0):
            move_player = (move_player[0] + self.game.player.x,
                           move_player[1] + self.game.player.y)
            other = self.cur_dungeon.collision_detect(*move_player, ignore=self.game.player)
            if not other:
                self.game.player.x, self.game.player.y = move_player
                self.game.player_move_finished()
            elif other != "dungeon":
                self.game.player.attack(other)
                self.game.player_move_finished()
        return True
        
    def draw(self):
        self.scr.clear()
        self.cur_dungeon.render(self.scr)
        self.scr.addch(self.game.player.y,
                       self.game.player.x,
                       "@")
        self.scr.noutrefresh()
