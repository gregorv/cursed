
import curses
import random

class Particle:
    def __init__(self, game, x, y, lifetime):
        self.game = game
        self.x = int(x)
        self.y = int(y)
        self.lifetime = int(lifetime)
        self.game.dungeon.cur_dungeon.particle_list.append(self)
    
    def animate(self):
        pass
    
    def on_character_touch(self, character):
        pass
    
    def render(self, scr):
        scr.chgat(self.y, self.x, 1, curses.color_pair(1))

class Fire(Particle):
    def __init__(self, game, x, y, lifetime, damage, sigma, mobile):
        Particle.__init__(self, game, x, y, lifetime)
        self.mobile = mobile
        self.damage = damage
        self.sigma = sigma
    
    def animate(self):
        if not self.mobile or random.random() < 0.7:
            return
        x = random.randint(self.x-1, self.x+1)
        y = random.randint(self.y-1, self.y+1)
        other = self.game.dungeon.cur_dungeon.collision_detect(x, y)
        if other == "dungeon":
            return
        self.x, self.y = x, y
    
    def on_character_touch(self, character):
        character.damage(random.gauss(self.damage, self.sigma))
    
    def render(self, scr):
        scr.chgat(self.y, self.x, 1, curses.color_pair(2))
        