"""
An IP Address is in the format of A.B.C.D, where A, B, C, D are all integers
between 0 to 255.

Given a string of numbers, return the possible IP addresses you can make with
that string by splitting into 4 parts of A, B, C, D.

Keep in mind that integers can't start with a 0! (Except for 0)

Example:

>>> sorted(OriginalSolution.ip_addresses("1592551013"))
['159.255.10.13', '159.255.101.3']

>>> sorted(OriginalSolution.ip_addresses("0000"))
['0.0.0.0']

>>> sorted(OriginalSolution.ip_addresses("00250"))
['0.0.2.50', '0.0.25.0']

>>> sorted(OriginalSolution.ip_addresses("0025"))
['0.0.2.5']

>>> sorted(OriginalSolution.ip_addresses("002"))
[]

>>> sorted(OriginalSolution.ip_addresses("1234567891234"))  # 13-char string
[]
"""

import unittest
from collections.abc import Generator, Iterable
from itertools import product
from typing import Protocol


class Solution(Protocol):
    @classmethod
    def ip_addresses(cls, s: str) -> Iterable[str]: ...


class OriginalSolution(Solution):
    """
    Generate all IP addresses that could be interpreted from a
    the string of digits `s`, where dots can be placed anywhere in the string.
    """

    @classmethod
    def multi_split(cls, n: int, s: str, ip_parts: list[str]) -> list[str]:
        result: list[str] = []
        for i in range(1, min(len(s), n) + 1):
            ip_parts.append(s[:i])
            result.extend(cls.ip_addresses_inner(s[i:], ip_parts))
            ip_parts.pop()

        return result

    @classmethod
    def ip_addresses_inner(cls, s: str, ip_parts: list[str]) -> list[str]:
        if not s:
            return []
        elif len(ip_parts) == 3:
            # there can only be one possibility
            if (
                len(s) == 1
                or (len(s) == 2 and s[0] != "0")
                or (len(s) == 3 and s <= "255" and s[0] != "0")
            ):
                ip_parts.append(s)
                result_elem: str = ".".join(ip_parts)
                ip_parts.pop()
                return [result_elem]
            else:
                return []

        match s[0]:
            case "0":
                # a 0 at the beginning can only be interpreted in one way
                ip_parts.append("0")
                result: list[str] = cls.ip_addresses_inner(s[1:], ip_parts)
                ip_parts.pop()
                return result
            case "1":
                return cls.multi_split(3, s, ip_parts)
            case "2":
                # integer can be between 1 and 3 digits
                # in the case of 3 digits, only integers up to 255 are allowed
                if len(s) < 3 or s[:3] > "255":
                    return cls.multi_split(2, s, ip_parts)
                else:
                    return cls.multi_split(3, s, ip_parts)
            case _:
                return cls.multi_split(2, s, ip_parts)

    @classmethod
    def ip_addresses(cls, s: str) -> list[str]:
        if len(s) < 4 or len(s) > 12:
            return []
        else:
            return cls.ip_addresses_inner(s, [])


class GeneratorSolution(Solution):
    """
    Generate the same result as `ip_addresses()`, but use a generator
    implementation instead. This was suggested by ChatGPT.
    """

    @classmethod
    def multi_split(cls, n: int, s: str, ip_parts: list[str]) -> Generator[str]:
        for i in range(1, min(len(s), n) + 1):
            ip_parts.append(s[:i])
            yield from cls.ip_addresses_inner(s[i:], ip_parts)
            ip_parts.pop()

    @classmethod
    def ip_addresses_inner(cls, s: str, ip_parts: list[str]) -> Generator[str]:
        if not s:
            return
        elif len(ip_parts) == 3:
            # there can only be one possibility
            if (
                len(s) == 1
                or (len(s) == 2 and s[0] != "0")
                or (len(s) == 3 and s <= "255" and s[0] != "0")
            ):
                ip_parts.append(s)
                yield ".".join(ip_parts)
                ip_parts.pop()

            return

        match s[0]:
            case "0":
                # a 0 at the beginning can only be interpreted in one way
                ip_parts.append("0")
                yield from cls.ip_addresses_inner(s[1:], ip_parts)
                ip_parts.pop()
            case "1":
                yield from cls.multi_split(3, s, ip_parts)
            case "2":
                # integer can be between 1 and 3 digits
                # in the case of 3 digits, only integers up to 255 are allowed
                if len(s) < 3 or s[:3] > "255":
                    yield from cls.multi_split(2, s, ip_parts)
                else:
                    yield from cls.multi_split(3, s, ip_parts)
            case _:
                yield from cls.multi_split(2, s, ip_parts)

    @classmethod
    def ip_addresses(cls, s: str) -> Generator[str]:
        if 4 <= len(s) <= 12:
            yield from cls.ip_addresses_inner(s, [])


class Tests(unittest.TestCase):
    solutions: list[type[Solution]] = [
        OriginalSolution,
        GeneratorSolution,
    ]

    cases: list[tuple[str, list[str]]] = [
        ("1592551013", ["159.255.10.13", "159.255.101.3"]),
        ("0000", ["0.0.0.0"]),
        ("00250", ["0.0.2.50", "0.0.25.0"]),
        ("0025", ["0.0.2.5"]),
        ("002", []),
        ("1234567891234", []),  # 13-char string
    ]

    def test_cases(self):
        for solution, (s, expected) in product(self.solutions, self.cases):
            sol: str = solution.__name__
            with self.subTest(solution=sol, s=s, expected=expected):
                self.assertEqual(expected, sorted(solution.ip_addresses(s)))


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    unittest.main()
