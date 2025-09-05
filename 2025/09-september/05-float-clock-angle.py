"""
Given a time in the format of hour and minute, calculate the angle of the hour
and minute hand on a clock.

Examples:

>>> clock_angle(3, 30)
75.0

>>> clock_angle(12, 30)
165.0

>>> clock_angle(4, 0)
-120.0

>>> clock_angle(9, 45)
-22.5
"""

import unittest

_DEGREES_PER_HOUR: float = 360 / 12  # 30
_DEGREES_PER_MINUTE_ON_HOUR: float = 360 / (60 * 12)  # 0.5
_DEGREES_PER_MINUTE: float = 360 / 60  # 6


def clock_angle(h: float, m: float) -> float:
    """
    Given a time `h:m`, calculate the angle created by the hour and minute
    hands of a clock. When the minute hand is behind the hour hand, a negative
    angle is returned.

    This has O(1) time and O(1) space complexity.
    """

    h_angle: float = h * _DEGREES_PER_HOUR + m * _DEGREES_PER_MINUTE_ON_HOUR
    m_angle: float = m * _DEGREES_PER_MINUTE
    return (m_angle - h_angle + 180) % 360 - 180


class Tests(unittest.TestCase):
    cases: list[tuple[float, float, float]] = [
        (3, 30, 75),
        (12, 30, 165),
        (4, 0, -120),
        (9, 45, -22.5),
    ]

    def test_cases(self):
        for h, m, expected in self.cases:
            with self.subTest(h=h, m=m, expected=expected):
                self.assertAlmostEqual(expected, clock_angle(h, m), places=7)


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    unittest.main()
