#!/bin/python3

'''Provides the `StaticBufferMatcher` (aliased as `BufferMatcher`) class'''

#> Imports
from .dynamic import DynamicBufferMatcher
#</Imports

#> Header >/
__all__ = ('BufferMatcher', 'StaticBufferMatcher')

class StaticBufferMatcher(DynamicBufferMatcher):
    '''
        An implementation of `SimpleBufferMatcher` that calculates
            and changes the value of `.lno` and `.cno` statically whenever the position changes
        This is better than `DynamicBufferMatcher` when `.lno` and `.cno` are
            accessed a lot, but worse when many position changes
            are made without needing to access `.lno` and `.cno`
    '''
    __slots__ = ('lno', 'cno')

    # Code note: this makes (in my opinion) unusual usage of descriptors,
    #  specifically how slots are also descriptors

    def __init__(self, *args, **kwargs):
        DynamicBufferMatcher.pos.__set__(self, 0) # set slot descriptor
        self.lno = 0
        self.cno = 0
        super().__init__(*args, **kwargs)

    pos = property(DynamicBufferMatcher.pos.__get__) # pos get method is the same as the slot get
    @pos.setter
    def pos(self, pos: int) -> None: # pos set method executes slot set and then recalculates lno and cno
        diff = self.pos - pos
        if not diff: return
        DynamicBufferMatcher.pos.__set__(self, pos) # set pos
        print(pos, diff)
        if diff > 0:
            self.lno -= self.data.count(b'\n', pos, pos+diff)
        else:
            self.lno += self.data.count(b'\n', pos+diff, pos)
        self.cno = super().cno

    # save_pos and load_pos are changed so as to not have to calculate lno and cno every time
    def save_pos(self) -> tuple[int, int, int]:
        return (self.pos, self.lno, self.cno)
    def load_pos(self, pos: tuple[int, int, int]) -> None:
        DynamicBufferMatcher.pos.__set__(self, pos[0])
        self.lno, self.cno = pos[1:]

BufferMatcher = StaticBufferMatcher
