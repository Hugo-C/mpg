import math

RED = [1., 0., 0., 1.]
GREEN = [0., 1., 0., 1.]
BLUE = [0., 0., 1., 1.]
WHITE = [1., 1., 1., 1.]
BLACK = [0., 0., 0., 1.]


def rotate(deg):
    theta = deg * 3.14 / 180.
    c = math.cos(theta)
    s = math.sin(theta)
    return [
        [c, -s, 0],
        [s, c, 0],
        [0, 0, 1]
    ]


def scale(x, y):
    return [
        [x, 0, 0],
        [0, y, 0],
        [0, 0, 1]
    ]


def matmul(X, Y):
    return [[sum(a * b for a, b in zip(X_row, Y_col)) for Y_col in zip(*Y)] for X_row in X]


def lerp(A, B, C):
    return (C * A) + ((1 - C) * B)


def random(previous_result):
    """A pseudo-random number generator used (B.B.S) since random can't be imported"""
    m = 11 * 23
    return previous_result ** 2 % m


def norm_random(random_number, max_value):
    """Turn a random number to a number between 0 and max_value """
    res = 0
    for i in range(100):
        bit = random_number & (1 << i)
        res = (res + bit) % 100
    res /= 100
    return res * max_value
