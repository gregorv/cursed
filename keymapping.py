
class Keymapping:
    def __init__(self):
        self.mapping = {}
        
    def import_mapping(self, cfg_dict):
        for action, key in cfg_dict.items():
            mod = key.startswith("^")
            code = key[1:2] if mod else key[0:1]
            self.mapping[action] = (code, mod)
        
    def __call__(self, action, code, mod):
        if action not in self.mapping:
            raise ValueError("Action not known")
        return (code, mod) == self.mapping[action]