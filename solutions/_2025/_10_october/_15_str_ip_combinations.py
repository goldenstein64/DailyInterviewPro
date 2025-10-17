"""
An IP Address is in the format of A.B.C.D, where A, B, C, D are all integers
between 0 to 255.

Given a string of numbers, return the possible IP addresses you can make with
that string by splitting into 4 parts of A, B, C, D.

Keep in mind that integers can't start with a 0! (Except for 0)

Example:

>>> sorted(ip_addresses("1592551013"))
['159.255.10.13', '159.255.101.3']

>>> sorted(ip_addresses("0000"))
['0.0.0.0']

>>> sorted(ip_addresses("00250"))
['0.0.2.50', '0.0.25.0']

>>> sorted(ip_addresses("0025"))
['0.0.2.5']

>>> sorted(ip_addresses("002"))
[]

>>> sorted(ip_addresses("1234567891234"))  # 13-char string
[]
"""


def multi_split(n: int, s: str, ip_parts: list[str]) -> list[str]:
    result: list[str] = []
    for i in range(1, min(len(s), n) + 1):
        ip_parts.append(s[:i])
        result.extend(ip_addresses_inner(s[i:], ip_parts))
        ip_parts.pop()

    return result


def ip_addresses_inner(s: str, ip_parts: list[str]) -> list[str]:
    if s == "":
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
            result: list[str] = ip_addresses_inner(s[1:], ip_parts)
            ip_parts.pop()
            return result
        case "1":
            return multi_split(3, s, ip_parts)
        case "2":
            # integer can be between 1 and 3 digits
            # in the case of 3 digits, only integers up to 255 are allowed
            if len(s) < 3 or s[1] > "5" or s[2] > "5":
                return multi_split(2, s, ip_parts)
            else:
                return multi_split(3, s, ip_parts)
        case _:
            return multi_split(2, s, ip_parts)


def ip_addresses(s: str) -> list[str]:
    if len(s) < 4 or len(s) > 12:
        return []
    else:
        return ip_addresses_inner(s, [])


if __name__ == "__main__":
    import doctest

    doctest.testmod()
