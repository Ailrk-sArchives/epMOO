from typing import Tuple


def discrete_interval(t: Tuple[int, int]):
    # Create the correct boundary for interger only interval.
    # NOTE: The algorithm still yields a float, so it is
    #   required to manually convert it into int when the parameter
    #   is used.
    # ex. (1, 8) become (-0.99, 7.99), so int get (0 - 7)
    lower, upper = t
    return (lower - 1.01, upper - 0.01)
