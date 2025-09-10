"""
You are given an array. Each element represents the price of a stock on that
particular day. Calculate and return the maximum profit you can make from buying
and selling that stock only once.

- Buying the stock must occur before selling it.
- You may choose not to buy or sell at all.

Example:

>>> buy_and_sell_gpt([9, 11, 8, 5, 7, 10])
5

Explanation: The optimal trade is to buy when the price is 5 and sell when it is
10, so the return value should be 5 (profit = 10 - 5 = 5).

"""

import unittest
from itertools import pairwise, product
from typing import Callable


def buy_and_sell(stocks: list[int]) -> int:
    """
    An attempt at the solution that takes a simple rolling sum of differences
    between prices, clamping at 0 for each change.

    This approach does not work for arrays where the best profit is behind a
    worse profit, like [5, 10, 8], where 8 - 5 overrides 10 - 5.
    """
    rolling_sum = 0
    for a, b in pairwise(stocks):
        rolling_sum = max(0, rolling_sum + b - a)

    return rolling_sum


def buy_and_sell_fix_gpt(stocks: list[int]) -> int:
    """
    My original solution fixed by ChatGPT. Keep an overall maximum of the
    rolling_sum and return it.
    """
    rolling_sum = max_profit = 0
    for a, b in pairwise(stocks):
        rolling_sum = max(0, rolling_sum + b - a)
        max_profit = max(max_profit, rolling_sum)

    return max_profit


def buy_and_sell_gpt(stocks: list[int]) -> int:
    """
    An implementation provided to me by ChatGPT: track the minimum price and
    the maximum profit so far.
    """
    min_price: int | None = None
    max_profit = 0
    for price in stocks:
        min_price = min(min_price, price) if min_price else price
        max_profit = max(max_profit, price - min_price)
    return max_profit


class Tests(unittest.TestCase):
    solutions: list[Callable[[list[int]], int]] = [
        # buy_and_sell,
        buy_and_sell_fix_gpt,
        buy_and_sell_gpt,
    ]

    cases: list[tuple[list[int], int]] = [
        ([], 0),
        ([3], 0),
        ([5, 10], 5),
        ([10, 5], 0),
        ([5, 2, 6, 10], 8),
        ([10, 2, 5, 3, 8], 6),
        ([10, 2, 5, 3, 8, 5], 6),
        ([1, 8, 3, 2, 10], 9),
        ([5, 6, 1, 2, 10], 9),
        ([5, 10, 4, 8], 5),
        ([5, 10, 8], 5),
        ([9, 11, 8, 5, 7, 10], 5),
    ]

    def test_cases(self):
        for solution, (stocks, expected) in product(self.solutions, self.cases):
            sol = solution.__name__
            with self.subTest(solution=sol, stocks=stocks, expected=expected):
                self.assertEqual(expected, solution(stocks))


if __name__ == "__main__":
    unittest.main()
