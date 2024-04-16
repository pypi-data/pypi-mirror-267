# comparable_pattern

A comparable string / regex object for flexible string comparisons.

Useful for making unit tests less brittle without extensive mocking of things like timestamps and hashes which maybe change from one run to another.

## Examples

```doctest
>>> p = compile("foo")
>>> c = ComparablePattern(p)
>>> p == "foo"
False
>>> c == "foo"
True
>>> c == "bar"
False

>>> c = "foo" + ComparablePattern(compile("\d{3}"))
>>> c == "foo"
False
>>> c == "123"
False
>>> c == "foo123"
True

>>> c = ComparablePattern(compile("\d{3}")) + "bar"
>>> c == "bar"
False
>>> c == "123"
False
>>> c == "123bar"
True

>>> c = ComparablePattern(compile("\d{3}")) + ComparablePattern(compile("\w{3}"))
>>> c == "123"
False
>>> c == "abc"
False
>>> c == "123abc"
True
```
