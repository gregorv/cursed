
 
class Inventory:
    def __init__(self, scr):
        self.scr = scr
        
    def handle_keypress(self, code, mod):
        return False
        
    def draw(self):
        self.scr.clear()
        self.scr.border()
        self.scr.addstr(1, 10, "Inventory", curses.A_BOLD)
        self.scr.refresh()

class Spells:
    def __init__(self, scr):
        self.scr = scr
        
    def handle_keypress(self, code, mod):
        return False
        
    def draw(self):
        self.scr.clear()
        self.scr.border()
        self.scr.addstr(1, 10, "Spells & Magic", curses.A_BOLD)
        self.scr.refresh()

class Dungeon:
    def __init__(self, scr):
        self.scr = scr
        
    def handle_keypress(self, code, mod):
        return False
        
    def draw(self):
        self.scr.clear()
        self.scr.refresh()
