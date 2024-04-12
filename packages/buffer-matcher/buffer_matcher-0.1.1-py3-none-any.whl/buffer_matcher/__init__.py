#!/bin/python3

'''Buffer matchers for more memory efficient matching of patterns, etc.'''

#> Package >/
__all__ = ('BufferMatcherBase', 'simple', 'dynamic', 'static',
           'SimpleBufferMatcher', 'DynamicBufferMatcher', 'StaticBufferMatcher')

from .base import BufferMatcherBase

from . import simple, dynamic, static

from .simple import SimpleBufferMatcher
from .dynamic import DynamicBufferMatcher
from .static import StaticBufferMatcher
