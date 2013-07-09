

item_list = [
    ("Potion", 1, "Health Poiton", {"effect": lambda self, quaffer: quaffer.heal(50)}),
    ("Potion", 2, "Large Health Poiton", {"effect": lambda self, quaffer: quaffer.heal(200)}),
    ("Sword", 10, "Wooden Sword", {"on_wield_attack": lambda self, wielder, target: target.damage(wielder.strength*2)}),
]