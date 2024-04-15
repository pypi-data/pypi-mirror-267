import os
from .meta import ConfigMetaClass

class config(metaclass = ConfigMetaClass):
    @classmethod
    def get(self, name, attr=False):
        if attr:
            return self.get_attr(name, attr)
        else:
            return self.parse_file(self.get_file(name))
