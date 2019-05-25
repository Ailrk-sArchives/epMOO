from typing import Tuple


def discrete_interval(t: Tuple[int, int]):
    # Create the correct boundary for interger only interval.
    # NOTE: The algorithm still yields a float, so it is
    #   required to manually convert it into int when the parameter
    #   is used.
    lower, upper = t
    return (lower, upper + 1)


