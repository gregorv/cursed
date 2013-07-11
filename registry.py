
class Registry(type):
    classes = {}
    
    def __new__(mcs, name, bases, dict):
        cls = type.__new__(mcs, name, bases, dict)
        if mcs.check_validity(name, bases, dict):
            mcs.classes[name] = cls
        return cls
