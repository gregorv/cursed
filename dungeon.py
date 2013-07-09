
class Dungeon:
    def __init__(self, level, max_x, max_y):
        self.level = level
        self.max_x = max_x
        self.max_y = max_y
        self.npc_list = []
        
    def collision_detect(self, x, y, ignore=None):
        if(x >= self.max_x-1 or y >= self.max_y-1
           or x < 1 or y < 1):
            return "dungeon"
        return None
        
    def generate(self):
        pass
    
    def populate(self):
        pass
    
    def on_enter(self):
        pass
    
    def on_exit(self):
        pass
        
    def render(self, scr):
        for y in range(1, self.max_y-1):
            scr.addstr(y, 1, "."*(self.max_x-2))