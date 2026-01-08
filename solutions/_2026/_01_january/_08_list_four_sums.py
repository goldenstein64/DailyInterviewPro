"""
Given a list of numbers, and a target number n, find all unique combinations of
`a`, `b`, `c`, `d`, such that `a + b + c + d = n`.

Examples:

>>> four_sum([1, 1, -1, 0, -2, 1, -1], 0)
[[-2, 0, 1, 1], [-1, -1, 1, 1]]
>>> four_sum([3, 0, 1, -5, 4, 0, -1], 1)
[[-5, -1, 3, 4]]
>>> four_sum([0, 0, 0, 0, 0], 0)
[[0, 0, 0, 0]]
"""


def four_sum(nums: list[int], target: int) -> list[list[int]]:
    """
    Brute force through all pairs of numbers, and find the last pair of numbers
    using two pointers.

    I copied the implementation from GeeksForGeeks.

    Source: https://www.geeksforgeeks.org/dsa/find-four-elements-that-sum-to-a-given-value-set-2/
    """

    nums.sort()
    result: list[list[int]] = []

    for i in range(len(nums) - 3):
        if i > 0 and nums[i - 1] == nums[i]:  # skip i duplicates
            continue

        for j in range(i + 1, len(nums) - 2):
            if j > i + 1 and nums[j - 1] == nums[j]:  # skip j duplicates
                continue

            k = j + 1
            l = len(nums) - 1

            total = nums[i] + nums[j]
            while k < l:
                kl_total = nums[k] + nums[l]
                total += kl_total
                if total < target:
                    k += 1
                elif total > target:
                    l -= 1
                else:
                    result.append([nums[i], nums[j], nums[k], nums[l]])
                    k += 1
                    l -= 1

                    while k < l and nums[k - 1] == nums[k]:  # skip k duplicates
                        k += 1
                    while k < l and nums[l] == nums[l + 1]:  # skip l duplicates
                        l -= 1

                total -= kl_total

    return result


if __name__ == "__main__":
    import doctest

    doctest.testmod()
