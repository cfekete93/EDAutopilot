#!/bin/python3

class _SingleLineWriter:
    @property
    def newline_on_close(self):
        return self._newline_on_close

    @newline_on_close.setter
    def newline_on_close(self, value):
        if type(value) is not bool:
            raise TypeError("newline_on_close must be a bool")
        self._newline_on_close = value

    @property
    def clear_on_close(self):
        return self._clear_on_close

    @clear_on_close.setter
    def clear_on_close(self, value):
        if type(value) is not bool:
            raise TypeError("clear_on_close must be a bool")
        self._clear_on_close = value

    def __init__(self, newline_on_close=True, clear_on_close=False):
        self._len = 0
        self.newline_on_close = newline_on_close
        self.clear_on_close = clear_on_close

    def print(self, *msgs, newline=False, clear=False):
        if clear:
            self._clear()
        if newline:
            self._len = 0
            print('')
        for msg in msgs:
            self._len += len(msg)
            print(msg, end='', flush=True)

    def __del__(self):
        if self.clear_on_close:
            self._clear()
        if self.newline_on_close:
            print('')

    def _clear(self):
        print('\b \b' * self._len, end='', flush=True)
        self._len = 0


# Globals exposed to users
slp = _SingleLineWriter()
