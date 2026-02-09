"""
We have a list of tasks to perform, with a cooldown period. We can do multiple
of these at the same time, but we cannot run the same task simultaneously.

Given a list of tasks, find how long it will take to complete the tasks in the
order they are input.

Example:

>>> # [1, _, _, 1, 2, _, 1]
>>> get_run_time(tasks=[1, 1, 2, 1], cooldown=2)
7

>>> # [1, 2, 3, 1, _, 3, 1, _, _, 1]
>>> get_run_time(tasks=[1, 2, 3, 1, 3, 1, 1], cooldown=2)
10
"""


def get_run_time(tasks: list[int], cooldown: int) -> int:
    """
    Calculate how long it will take to run an ordered list of tasks with a given
    cooldown.

    This has roughly O(len(tasks)) time and O(min(cooldown, len(unique(tasks)))) space.
    """
    cooldowns: dict[int, int] = {}
    removed_keys: set[int] = set()
    result: int = 0
    for task in tasks:
        task_cooldown: int = cooldowns.get(task, 0) + 1
        result += task_cooldown
        removed_keys.clear()
        for k, v in cooldowns.items():
            if v <= task_cooldown:
                removed_keys.add(k)
            else:
                cooldowns[k] = v - task_cooldown

        for k in removed_keys:
            del cooldowns[k]
        cooldowns[task] = cooldown

    return result


if __name__ == "__main__":
    import doctest

    doctest.testmod()
