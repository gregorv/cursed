""
"""
    This file is part of Cursed
    Copyright (C) 2013 Gregor Vollmer <gregor@celement.de>

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

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