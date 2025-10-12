"""
Given a file path with folder names, '..' (Parent directory), and '.' (Current
directory), return the shortest possible file path (Eliminate all the '..' and
'.').

Example:

>>> shortest_path("/Users/Joma/Documents/../Desktop/./../")
'/Users/Joma/'
"""


def shortest_path(file_path: str) -> str:
    """
    Normalize an absolute file path containing '..' and '.'.

    This uses O(n) time and O(n) space, where n is the number of folders.
    """
    if file_path[0] == "/":
        file_path = file_path[1:]

    if file_path[-1] == "/":
        file_path = file_path[:-1]

    result: list[str] = []
    for folder in file_path.split("/"):
        if folder == "..":
            result.pop()
        elif folder != ".":
            result.append(folder)

    return f"/{"/".join(result)}/"


if __name__ == "__main__":
    import doctest

    doctest.testmod()
