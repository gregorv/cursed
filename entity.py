
class Entity:
    """
    Things knowing the concept of life and the space-time.
    """
    def __init__(self, game):
        self.game = game
        self.hp = 100
        self.pos = (1, 1)
        self.symbol = " "
        self.round_cooldown = 0
        
    def set_round_cooldown(self, time_required):
        self.round_cooldown = int(time_required)
        