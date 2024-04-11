#!/bin/python3

'''Provides the `SimpleBufferMatcher` (aliased as `BufferMatcher`) class'''

#> Imports
import io
import re
import typing
from abc import abstractproperty
from functools import singledispatchmethod
from collections import abc as cabc

from .base import BufferMatcherBase
#</Imports

#> Header >/
__all__ = ('BufferMatcher', 'SimpleBufferMatcher')

class SimpleBufferMatcher(BufferMatcherBase):
    '''
        Provides a partial implementation of `BufferMatcher`,
            with abstracts to keep track of line and column numbers
    '''
    __slots__ = ('data', 'len', 'pos')

    view: memoryview | None
    data: bytes
    len: int
    pos: int

    @abstractproperty
    def lno(self) -> int: pass
    @abstractproperty
    def cno(self) -> int: pass

    def __init__(self, data: bytes, *, copy_mode: bool = False):
        self.data = data
        self.view = memoryview(self.data)
        self.len = len(self.data)
        self.pos = 0
        super().set_mode(copy_mode)
    def __len__(self) -> int:
        '''Returns the total length of the given data'''
        return self.len

    def close(self) -> None:
        '''
            Calls the superclass `.close()`,
                nulls the underlying data,
                and releases the memoryview
        '''
        if self.closed: return
        super().close()
        self.data = None
        if self.view is None: return
        self.view.release()
        self.view = None

    def view_read(self, size: int = -1, /) -> memoryview:
        if self.closed:
            raise ValueError('Cannot perform operation on closed BufferMatcher')
        if self.view is None:
            raise BufferError('Cannot perform operation: missing view (view was detached?)')
        if size < 0:
            data = self.view[self.pos:self.len]
            self.pos = self.len
            return data
        data = self.view[self.pos:self.pos+size]
        self.pos = min(self.pos + size, self.len)
        return data

    def view_readline(self, size: int = -1, /) -> memoryview:
        if self.closed:
            raise ValueError('Cannot perform operation on closed BufferMatcher')
        if self.view is None:
            raise BufferError('Cannot perform operation: missing view (view was detached?)')
        try: index = self.data.index(b'\n', self.pos)
        except ValueError: # EOF
            return self.view_read(size)
        if size < 0:
            return self.view_read(index - self.pos)
        return self.view_read(min(index - self.pos, size))

    def view_peek(self, size: int = -1, /) -> memoryview:
        if self.closed:
            raise ValueError('Cannot perform operation on closed BufferMatcher')
        if self.view is None:
            raise BufferError('Cannot perform operation: missing view (view was detached?)')
        if size < 0:
            return self.view[self.pos:self.len]
        return self.view[self.pos:self.pos+size]

    def seek(self, offset: int, whence: typing.Literal[io.SEEK_SET, io.SEEK_CUR, io.SEEK_END], *, strict: bool = False) -> int:
        '''
            Seeks to(wards) `offset` from `whence`
            If `strict`, then fails (`IndexError` or `EOFError`) when trying to seek out of bounds,
                otherwise seeks to the nearest boundary (`0` or EOF)
        '''
        if self.closed:
            raise ValueError('Cannot perform operation on closed BufferMatcher')
        if self.view is None:
            raise BufferError('Cannot perform operation: missing view (view was detached?)')
        match whence:
            case io.SEEK_SET:
                if strict and (offset < 0):
                    raise IndexError('Cannot seek negatively with SEEK_SET when strict is true')
                pos = self.len + offset
            case io.SEEK_CUR:
                pos = self.pos + offset
            case io.SEEK_END:
                if strict and (offset > 0):
                    raise EOFError('Cannot seek positively with SEEK_END when strict is true')
                pos = self.len + offset
        if pos < 0:
            if strict: raise IndexError('Cannot seek to negative position when strict is true')
            pos = 0
        if pos > self.len:
            if strict: raise EOFError('Cannot seek past end of file')
            pos = self.len
        self.pos = pos
    def tell(self) -> int:
        if self.closed:
            raise ValueError('Cannot perform operation on closed BufferMatcher')
        if self.view is None:
            raise BufferError('Cannot perform operation: missing view (view was detached?)')
        return self.pos

    def save_pos(self) -> int:
        '''
            Saves the current position as an object
            The type and value of this object should not be considered
                as a stable interface, and should only be used for `.load_pos()`
                More specifically, the object itself is considered unstable,
                    but `.load_pos()` loading positions from `.save_pos()` (assuming the underlying data is the same)
                    should result in the same position
                TL,DR: use these methods for their intended purpose, do not use or modify the
                    object for any other uses
                If you want position information, use `.tell()`/`.pos` and `.lno`/`.cno`
        '''
        return self.pos
    def load_pos(self, pos: int) -> None:
        '''
            Loads the position from an object saved by `.save_pos()`
            The type of `pos`, as well as the behavior of `.load_pos()`,
                should not be considered part of the stable interface
                More specifically, the object itself is considered unstable,
                    but `.load_pos()` loading positions from `.save_pos()` (assuming the underlying data is the same)
                    should result in the same position
                TL,DR: use these methods for their intended purpose, do not use or modify the
                    object for any other uses
                If you want position information, use `.tell()`/`.pos` and `.lno`/`.cno` instead
        '''
        self.pos = pos

    @singledispatchmethod
    def view_match(self, to: typing.Any) -> memoryview | typing.Any:
        raise TypeError(f'Cannot match to object {type(to).__qualname__} (of {to!r})')
    @view_match.register
    def match_callable(self, to: cabc.Callable) -> memoryview | typing.Any:
        '''
            Matches to a callable
            The callable should take a memoryview, and outputs the amount of to advance,
                and the result
                It should have the following signature: `(data: memoryview) -> tuple[int | None, typing.Any]`
        '''
        size,res = to(self.view[self.pos:])
        if size is None: return res
        self.step(size)
        return res
    @view_match.register
    def match_pattern(self, to: re.Pattern) -> re.Match | None:
        '''Matches to a pattern'''
        m = to.match(self.view[self.pos:])
        if m is not None: self.step(m.end())
        return m
    @view_match.register
    def match_string(self, to: bytes) -> bytes | None:
        '''Matches to a string (of bytes)'''
        if self.peek(len(to)) == to:
            self.step(len(to))
            return to
        return None

BufferMatcher = SimpleBufferMatcher
