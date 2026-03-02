"""
The power function calculates x raised to the nth power. If implemented in O(n)
it would simply be a for loop over n and multiply x n times. Instead implement
this power function in O(log n) time. You can assume that n will be a
non-negative integer.

Example:

>>> pow_iter(5, 3)
125

>>> pow_iter(2, 10)
1024
"""


def pow(x: int, p: int) -> int:
    """
    Return `x` to the power of `p`. This uses two identities to implement the
    function in O(log n) time:

    if even(p): x**p = (x**(p//2))**2
    else if odd(p): x**p = x * (x**(p//2))**2
    """

    if p == 0:
        return 1
    elif p == 1:
        return x

    half = pow(x, p // 2)
    if p % 2 == 0:
        return half * half
    else:
        return x * half * half


def pow_iter(x: int, p: int) -> int:
    if p == 0:
        return 1

    result: int = x
    while p > 1:
        result = result * result
        if p % 2 == 1:
            result *= x

        p //= 2

    return result


if __name__ == "__main__":
    import doctest

    doctest.testmod()
