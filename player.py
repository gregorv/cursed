
from entity import Entity
from item import Inventory
import math

class Player(Entity):
    def __init__(self, game):
        Entity.__init__(self, game)
        self.name = "Adventurer"
        self.mana = 0
        self.char_skills = {
            "max_hp": 20,
            "max_mana": 20,
            "hp_regen": 1,
            "mana_regen": 1,
            "strength": 1,
        }
        self.inventory = Inventory
        
    def handle_keypress(self, code, mod):
        move = (0, 0)
        if self.game.keymap("player.w", code, mod): move = (-1, 0)
        elif self.game.keymap("player.e", code, mod): move = (1, 0)
        elif self.game.keymap("player.n", code, mod): move = (0, -1)
        elif self.game.keymap("player.s", code, mod): move = (0, 1)
        elif self.game.keymap("player.ne", code, mod): move = (1, -1)
        elif self.game.keymap("player.nw", code, mod): move = (-1, -1)
        elif self.game.keymap("player.se", code, mod): move = (1, 1)
        elif self.game.keymap("player.sw", code, mod): move = (-1, 1)
        elif self.game.keymap("player.pickup", code, mod):
            if self.pos in self.game.map.item_piles:
                self.game.set_view("PickupItems",
                                   self.game.map.item_piles[self.pos])
        else:
            return False
        
        if move != (0, 0):
           new = move[0] + self.pos[0], move[1] + self.pos[1]
           detect = self.game.map.collision_detect(new)
           if detect is None:
               self.pos = new
               self.set_round_cooldown(math.sqrt((10*move[0])**2 + (10*move[1])**2))

character_skills = (
    ("max_hp", 20, "Max HP", "Maximum HP"),
    ("max_mana", 20, "Max Mana", "Maximum Mana"),
    ("hp_regen", 1, "HP Regen", "Regeneration of HP per round"),
    ("mana_regen", 1, "Mana Rege", "Regeneration of Mana per round"),
    ("strength", 1, "Strength", "Strength of physical attacks"),
    ("spell_casting", 1, "Spell Casting")
)