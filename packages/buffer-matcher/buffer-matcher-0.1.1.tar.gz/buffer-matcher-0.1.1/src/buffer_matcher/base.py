#!/bin/python3

'''Implements the base type for buffer matchers'''

#> Imports
import io
import typing
from abc import abstractmethod
from collections import abc as cabc
#</Imports

#> Header >/
__all__ = ('BufferMatcherBase',)

class BufferMatcherBase(io.BufferedIOBase):
    '''
        Provides a base for buffer matching
        By default, results of operations that can return memoryviews will return them to conserve memory
            This can be changed by executing `.set_mode()`,
                which will replace all base methods with their "copy" equivelant, or by using the methods prefixed with `copy_`,
                instead of the `view_` methods
    '''
    __slots__ = ('view', 'copy_mode',
                 'read', 'readline', 'peek')

    view: memoryview | None
    copy_mode: bool

    @abstractmethod
    def __init__(self): pass

    def set_mode(self, copy: bool = False) -> None:
        '''Sets "copy" mode, where functions will return bytes instead of memoryviews'''
        self.copy_mode = copy
        if self.copy_mode:
            self.read = self.copy_read
            self.readline = self.copy_readline
            self.peek = self.copy_peek
            self.match = self.copy_match
        else:
            self.read = self.view_read
            self.readline = self.view_readline
            self.peek = self.view_peek
            self.match = self.view_match

    @abstractmethod
    def close(self) -> None: pass
    def detach(self) -> memoryview:
        '''
            Detatches the underlying memoryview, making this object unusable
            Note that, unlike `.close()`, this will not release the memory
            It is recommended to call `.close()` after this method
        '''
        view = self.view
        self.view = None
        return self.view

    def readable(self) -> bool:
        return True

    @abstractmethod
    def view_read(self, size: int = -1, /) -> memoryview:
        '''Reads `size` bytes or to EOF'''
    def copy_read(self, size: int = -1, /) -> bytes:
        '''See `.view_read()`'''
        return self.view_read(size).tobytes()
    read: cabc.Callable[[int], memoryview | bytes]

    def read1(self) -> typing.NoReturn:
        '''Not used--raises `io.UnsupportedOperation`'''
        raise io.UnsupportedOperation('read1')

    @abstractmethod
    def view_readline(self, size: int = -1, /) -> memoryview:
        '''
            Reads until newline or EOF, including newline if present
            If `size` is specified, returns at most `size` characters
        '''
    def copy_readline(self, size: int = -1, /) -> bytes:
        '''See `.view_readline()'''
        return self.view_readline(size).tobytes()
    readline: cabc.Callable[[int], memoryview | bytes]

    @abstractmethod
    def view_peek(self, size: int = -1, /) -> memoryview:
        '''Look ahead up to `size` bytes without advancing position'''
    def copy_peek(self, size: int = -1, /) -> bytes:
        '''See `.view_peek()`'''
        return self.view_peek(size).tobytes()
    peek: cabc.Callable[[int], memoryview | bytes]

    @abstractmethod
    def seek(self, offset: int, whence: typing.Literal[io.SEEK_SET, io.SEEK_CUR, io.SEEK_END] = io.SEEK_SET) -> int: pass
    def step(self, offset: int = 1) -> int:
        '''Convenience method to `seek()` with `whence` set to `io.SEEK_CUR`'''
        return self.seek(offset, io.SEEK_CUR)
    @abstractmethod
    def tell(self) -> int:
        '''Returns the current position'''

    @abstractmethod
    def view_match(self, to: typing.Any) -> memoryview | typing.Any:
        '''Tries to match to `to`, depending on its type'''
    def copy_match(self, to: typing.Any) -> bytes | typing.Any:
        '''
            See `.match_view()`
            Note that if `.match_view()` returns a memoryview, this method
                can automatically convert it, but not any other type
        '''
        res = self.match_view(to)
        return res.tobytes() if isinstance(res, memoryview) else res
    match: cabc.Callable[[typing.Any], typing.Any]
