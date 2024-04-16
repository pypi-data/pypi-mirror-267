from __future__ import annotations

from re import compile, Pattern, escape
from typing import Any


class ComparablePattern:
    r"""
    A regular expression object that can be compared to a string using `==` or using `assertEqual` in unit tests.

    Since `Pattern` can't be extended, we simply wrap it.

    Examples:
        >>> p = compile("foo")
        >>> c = ComparablePattern(p)
        >>> p == "foo"
        False
        >>> c == "foo"
        True
        >>> c == "bar"
        False

        >>> c = "foo" + ComparablePattern(compile("\\d{3}"))
        >>> c == "foo"
        False
        >>> c == "123"
        False
        >>> c == "foo123"
        True

        >>> c = ComparablePattern(compile("\\d{3}")) + "bar"
        >>> c == "bar"
        False
        >>> c == "123"
        False
        >>> c == "123bar"
        True

        >>> c = ComparablePattern(compile("\\d{3}")) + ComparablePattern(compile("\\w{3}"))
        >>> c == "123"
        False
        >>> c == "abc"
        False
        >>> c == "123abc"
        True
    """

    pattern: Pattern[str]

    def __init__(self, pattern: Pattern[str]) -> None:
        self.pattern = pattern

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, str):
            return self.pattern.match(other) is not None
        return super().__eq__(other)

    @staticmethod
    def _get_pattern(other: Any) -> str:
        if isinstance(other, str):
            other_pattern = escape(other)
        elif isinstance(other, Pattern):
            other_pattern = other.pattern
        elif isinstance(other, ComparablePattern):
            other_pattern = other.pattern.pattern
        else:
            raise NotImplementedError()
        return other_pattern

    def __radd__(self, other: Any) -> ComparablePattern:
        return ComparablePattern(
            compile(self._get_pattern(other) + self.pattern.pattern)
        )

    def __add__(self, other: Any) -> ComparablePattern:
        return ComparablePattern(
            compile(self.pattern.pattern + self._get_pattern(other))
        )

    def __repr__(self) -> str:
        return self.pattern.__repr__()
