
RED = [1., 0., 0., 1.]
GREEN = [0., 1., 0., 1.]
BLUE = [0., 0., 1., 1.]
WHITE = [1., 1., 1., 1.]
BLACK = [0., 0., 0., 1.]


def lerp(A, B, C):
    return (C * A) + ((1 - C) * B)


def random(previous_result):
    """A pseudo-random number generator used (B.B.S) since random can't be imported"""
    m = 11 * 23
    return previous_result ** 2 % m


def norm_random(random_number):
    """Turn a random number to a number between 0 and max_value """
    precision = 20
    res = 0.
    for i in range(precision):
        bit = random_number & (1 << i)
        res += bit
    res %= precision
    res /= precision
    return res
