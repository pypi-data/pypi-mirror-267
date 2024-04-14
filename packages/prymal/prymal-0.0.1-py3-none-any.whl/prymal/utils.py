import math


def square_root_newton(n, k=10):
    x = n >> (len(bin(n)) // 2)
    for _ in range(k):
        x = (x ** 2 + n) // (2 * x)
    return x
