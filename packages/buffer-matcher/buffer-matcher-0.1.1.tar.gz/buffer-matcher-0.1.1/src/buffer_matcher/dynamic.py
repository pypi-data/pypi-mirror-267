#!/bin/python3

'''Provides the `DynamicBufferMatcher` (aliased as `BufferMatcher`) class'''

#> Imports
from .simple import SimpleBufferMatcher
#</Imports

#> Header >/
__all__ = ('BufferMatcher', 'DynamicBufferMatcher')

class DynamicBufferMatcher(SimpleBufferMatcher):
    '''
        An implementation of `SimpleBufferMatcher` that dynamically
            calculates line and column numbers (`.lno`, `.cno`) upon request
    '''
    __slots__ = ()

    @property
    def lno(self) -> int:
        return self.data.count(b'\n', 0, self.pos)
    @property
    def cno(self) -> int:
        try: lastline = self.data.rindex(b'\n', 0, self.pos)
        except ValueError: lastline = 0
        return self.pos - lastline

BufferMatcher = DynamicBufferMatcher
