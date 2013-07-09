
import curses

import gamescr
import character

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
        self.scr.noutrefresh()
        
    def handle_keypress(self, code, mod):
        return False
    
    def log(self, msg):
        self.history.append(msg[:self.maxmsglen] if len(msg) > self.maxmsglen else msg)
        while(len(self.history) > self.maxlog):
            del self.history[0]
            
    def __call__(self, msg):
        self.log(msg)

class Game:
    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.mainscr = curses.newwin(20, 59, 0, 0)
        self.infoscr = curses.newwin(20, 20, 0, 60)
        self.messagescr = curses.newwin(5, 80, 20, 0)
        
        self.player = character.Player(self)
        self.round = 1
       
        self.quit = False
        
        self.game_screens = {}
        screen_factory = [gamescr.Dungeon, gamescr.Inventory, gamescr.Spells]
        for i, scr in enumerate(screen_factory):
            tmp = scr(self, self.mainscr)
            self.game_screens[tmp.name] = tmp
            if i == 0:
                self.dungeon = tmp
        self.logger = Logger(self.messagescr)
        self.active_game_screen = self.dungeon
        
    def player_move_finished(self):
        self.round += 1
        self.player.hp = min(self.player.max_hp, self.player.hp + self.player.regen)
        old = self.player.mana
        self.player.mana = min(self.player.max_mana, self.player.mana + self.player.mana_regen)
        self.player.mana_regen_bonus += (self.player.mana - old) * 0.01
        self.dungeon.cur_dungeon.update()
        
    def set_active(self, new_active=""):
        self.active_game_screen.on_deactivate()
        if new_active:
            self.active_game_screen = self.game_screens[new_active]
        else:
            self.active_game_screen = self.dungeon   
        self.active_game_screen.on_activate()
    
    def _draw_info(self):
        self.infoscr.clear()
        self.infoscr.border()
        self.infoscr.addstr(1, 1,"HP  {p.hp}/{p.max_hp}".format(p=self.player))
        self.infoscr.addstr(2, 1,"MNA {p.mana}/{p.max_mana}".format(p=self.player))
        self.infoscr.addstr(3, 1,"STR {p.strength}".format(p=self.player))
        self.infoscr.addstr(3, 10,"SPR {p.spirit}".format(p=self.player))
        self.infoscr.addstr(4, 1,"RGN {p.regen}".format(p=self.player))
        self.infoscr.addstr(4, 10,"MRG {p.mana_regen}".format(p=self.player))
        self.infoscr.addstr(5, 1,"EXP {p.exp} -> {p.exp_next_level}".format(p=self.player))
        self.infoscr.addstr(6, 1,"LVL {p.level}".format(p=self.player))
        self.infoscr.addstr(8, 1,"Wielded:")
        self.infoscr.addstr(9, 2,"{0}".format(self.player.in_hands.name
                                                        if self.player.in_hands
                                                        else "nothing"))
        self.infoscr.addstr(10, 1,"Armour:")
        self.infoscr.addstr(11, 2,"+{0} {1}".format(self.player.armour.defense
                                                        if self.player.armour
                                                        else "0",
                                                        self.player.armour.name
                                                        if self.player.armour
                                                        else ""))
        self.infoscr.addstr(13, 1,"Dungeon Level {0}".format(self.dungeon.level))
        self.infoscr.addstr(14, 1,"Round {0}".format(self.round))
        
        if self.player.last_enemy:
            self.infoscr.addstr(16, 1,"{e.name}".format(e=self.player.last_enemy))
            self.infoscr.addstr(18, 1,"HP {e.hp}/{e.max_hp}".format(e=self.player.last_enemy))
            self.infoscr.addstr(17, 1,"LVL {e.level}".format(e=self.player.last_enemy))
        self.infoscr.noutrefresh()
        
    def handle_keypress(self, code, mod):
        if mod and code == "q":
            self.quit = True
        else:
            return False
        return True
        
    def draw(self):
        self._draw_info()
        self.logger.draw()
        self.active_game_screen.draw()
        curses.doupdate()

    def run(self):
        while not self.quit:
            self.draw()
            curses.doupdate()
            self.player.last_enemy
            mod = False
            code = self.mainscr.getkey()
            if code == "\x1b":
                mod = True
                while code == "\x1b":
                    code = self.stdscr.getkey()
            key_listeners = [self, self.logger, self.active_game_screen]
            if self.player.hp == 0:
                key_listeners = [self]
            for listener in key_listeners:
                if listener.handle_keypress(code, mod):
                    break
            else:
                self.logger.log("Unhandled keypress {1}{0}".format(repr(code), "mod " if mod else ""))