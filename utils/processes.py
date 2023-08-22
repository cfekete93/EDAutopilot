#!/bin/python3

# Needed because forward references are not allowed in return type hints
from __future__ import annotations

# System libraries
from multiprocessing.managers import SharedMemoryManager
from multiprocessing.shared_memory import ShareableList

# Globals
_attributes = 0


# Dynamically register the number attributes belonging to the SharedObject
def _register(f):
    global _attributes
    _attributes += 1
    return f


class SharedObject:
    @classmethod
    def create(cls, smm: SharedMemoryManager) -> SharedObject:
        global _attributes
        sl = smm.ShareableList(range(_attributes))
        return cls(sl)

    def __init__(self, sl: ShareableList):
        self._sl = sl

    def __del__(self):
        pass

    # TODO [Chris]: Perhaps _register can take the positional argument too and supply it in setter?
    @_register
    @property
    def x(self):
        return self._sl[0]

    @x.setter
    def x(self, value):
        self._sl[0] = value

    # TODO [Chris]: Perhaps _register can take the positional argument too and supply it in setter?
    @property
    @_register
    def y(self):
        return self._sl[1]

    @y.setter
    def y(self, value: str):
        self._sl[1] = value

    # TODO [Chris]: Perhaps _register can take the positional argument too and supply it in setter?
    @property
    @_register
    def z(self):
        return self._sl[2]

    @z.setter
    def z(self, value):
        self._sl[2] = value
