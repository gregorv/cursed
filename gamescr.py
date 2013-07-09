
import curses
import dungeon

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
    pass

class Spells(BaseScreen):
    
    def draw(self):
        self.scr.clear()
        self.scr.border()
        self.scr.addstr(1, 10, "Spells & Magic", curses.A_BOLD)
        self.scr.noutrefresh()

class Dungeon(BaseScreen):
    def __init__(self, game, scr):
        BaseScreen.__init__(self, game, scr)
        self.level = 1
        max_y, max_x = self.scr.getmaxyx()
        self.dungeons = {1: dungeon.Dungeon(1, max_x, max_y)}
        self.cur_dungeon = self.dungeons[self.level]
        
    def next_dungeon(self):
        self.dungeons[self.level].on_exit()
        self.level += 1
        if self.level not in self.dungeons:
            max_y, max_x = self.scr.getmaxyx()
            self.dungeons[self.level] = dungeon.Dungeon(self, self.level, max_x, max_y)
        self.dungeons[self.level].on_enter()
        self.cur_dungeon = self.dungeons[self.level]
        
    def prev_dungeon(self):
        if self.level == 1:
            return
        self.dungeons[self.level].on_exit()
        self.level -= 1
        self.dungeons[self.level].on_enter()
        self.cur_dungeon = self.dungeons[self.level]
    
    def handle_keypress(self, code, mod):
        move_player = 0, 0
        if mod:
            if code == "q": self.game.quit = True
            else:
                return BaseScreen.handle_keypress(self, code, mod)
        else:
            if code == "i": self.game.set_active("Inventory")
            elif code == "x": self.game.set_active("Spells")
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
            else:
                return BaseScreen.handle_keypress(self, code, mod)
        if move_player != (0, 0):
            move_player = (move_player[0] + self.game.player.x,
                           move_player[1] + self.game.player.y)
            other = self.cur_dungeon.collision_detect(*move_player, ignore=self.game.player)
            if not other:
                self.game.player.x, self.game.player.y = move_player
        return True
        
    def draw(self):
        self.scr.clear()
        self.cur_dungeon.render(self.scr)
        self.scr.addch(self.game.player.y,
                       self.game.player.x,
                       "H")
        self.scr.noutrefresh()
