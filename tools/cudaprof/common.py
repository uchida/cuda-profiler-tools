# Author: Javier Cabezas <javier.cabezas@bsc.es>
#
# Copyright (c) 2013 Barcelona Supercomputing Center
#                    IMPACT Research Group
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

def enum(**enums):
    return type('Enum', (), enums)


class Option:
    def __init__(self, name, out = 1, value = None):
        self.name        = name
        self.description = "" # TODO: fill this field
        self.out         = out
        self.value       = value

        self.active = False

    def __repr__(self):
        if self.value != None:
            return '%s=%s' % (self.name, self.value)
        else:
            return '%s' % (self.name)

    def set_active(self, active):
        self.active = active


class Counter(object):
    def __init__(self, name, description, category, id):
        self.name        = name
        self.description = description
        self.category    = category

        self.id     = id
        self.active = False

    def __repr__(self):
        ret = 'Counter: %s' % (self.name)
        return ret

    def set_active(self, active):
        self.active = active

    def is_internal(self):
        return self.name[0:2] == '__'


COUNTER_CATEGORIES = { 0: 'Instruction',
                       1: 'Memory',
                       2: 'Cache',
                       3: 'Profile trigger'
                      }

# vim:set backspace=2 tabstop=4 shiftwidth=4 textwidth=120 foldmethod=marker expandtab: