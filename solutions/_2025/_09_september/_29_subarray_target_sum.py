"""
You are given an array of integers, and an integer K. Return the subarray which
sums to K. You can assume that a solution will always exist.

Example:

>>> find_continuous_k_sliding_window([1, 3, 2, 5, 7, 2], 14)
[2, 5, 7]
>>> find_continuous_k_prefix_sum([1, -3, 2, -5, 7, -2], 4)
[2, -5, 7]
"""


def find_continuous_k_sliding_window(nums: list[int], k: int) -> list[int]:
    """
    Find a continuous slice of `nums` that adds up to `k`. This only works when
    all integers in `nums` is positive.

    This has O(n) time complexity and O(1) space.
    """
    if k == 0:
        return []

    i: int = 0
    rolling: int = 0
    for j, num in enumerate(nums):
        rolling += num
        while rolling > k:
            rolling -= nums[i]
            i += 1

        if rolling == k:
            return nums[i : j + 1]

    raise ValueError("subarray sum not found")


def find_continuous_k_prefix_sum(nums: list[int], k: int) -> list[int]:
    """
    Find a continuous slice of `nums` that adds up to `k`. This uses a
    dictionary `prefix_sums` to hold all sums made up of slices `nums[0:j]`. If
    `i := prefix_sums[rolling - k]` is valid, then `nums[0:j] - nums[0:i] == k`,
    meaning a slice `nums[i:j]` was found.

    This has O(n) time complexity and O(n) space.
    """
    rolling: int = 0
    prefix_sums: dict[int, int] = {0: 0}
    for j, num in enumerate(nums, start=1):
        rolling += num
        prefix_sums[rolling] = j
        if (i := prefix_sums.get(rolling - k)) is not None:
            return nums[i:j]

    raise ValueError("subarray sum not found")


if __name__ == "__main__":
    import doctest

    doctest.testmod()
