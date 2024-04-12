Buffer matchers, as I refer to them, are wrappers around bytes that
allow easier, more memory-efficient reading and pattern matching

These are used in my programming language [Caustic](https://codeberg.org/Caustic)'s [Lexer](https://codeberg.org/Caustic/CausticLexer)

Beyond base classes, this package provides two buffer matcher classes:
- `DynamicBufferMatcher` / `dynamic.BufferMatcher`
- `StaticBufferMatcher` / `static.BufferMatcher`

The buffer classes shown above can be `.read()`, `.seek()`ed through,
and `.match()`ed against strings, callables, or regular expressions

The "dynamic" and "static" in the names refer to how they calculate
line and column numbers -- namely, the "dynamic" buffer matcher
calculates line and column numbers via properties, every time
they are accessed; whilst the "static" buffer matcher calculates
line and column numbers only when the position of the matcher is
changed. "Dynamic" buffer matchers are recommended if line and column
numbers are accessed less often than the position is changed, and vice-versa
for "static" buffers. 

# Changelog

## v0.1.1
- Fixed `SimpleBufferMatcher.copy_peek()` ignoring `size` parameter
