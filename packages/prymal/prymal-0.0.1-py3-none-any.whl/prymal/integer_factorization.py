from .sieve import eratosthenes
from itertools import cycle

import math
import random


def trial_division(n: int) -> int:
    '''
    Performs trial division integer factorization

    Parameters:
    n (int): Positive composite number

    Returns:
    d (int): One non trivial factor of n
    '''

    if n % 2 == 0:
        return 2

    d = 3
    while d ** 2 <= n:
        if n % d == 0:
            return d
        d += 2

    raise ValueError('failed to find factor, maybe n is prime.')


def wheel_factorization(n: int) -> int:
    '''
    Performs wheel factorization

    Parameters:
    n (int): Positive composite number

    Returns:
    d (int): One non trivial factor of n
    '''

    basis = []
    if n <= 100000:
        basis = [2, 3]
    else:
        basis = [2, 3, 5, 7]

    for p in basis:
        if n % p == 0:
            return p

    product = 1
    for p in basis:
        product *= p

    wheel = []
    for wheel_candidate in range(max(basis) + 1, product + 2):
        for p in basis:
            if wheel_candidate % p == 0:
                break
        else:
            wheel.append(wheel_candidate)

    increments = [b - a for a, b in zip(wheel[:-1], wheel[1:])]

    d = wheel[0]
    for increment in cycle(increments):
        d += increment
        if d * d > n:
            return n
        elif n % d == 0:
            return d


def pollards_rho(n: int, n_attempts: int=10) -> int:
    '''
    Performs Pollard's rho integer factorization

    Parameters:
    n (int): Positive composite number
    n_attempts (int): Number of retries upon factorization failure

    Returns:
    d (int): One non trivial factor of n or n upon failure
    '''

    x = random.randint(0, n - 1)
    y = x
    d = 1
    b = random.randint(1, n - 3)

    def g(x):
        return (x ** 2 + b) % n

    while d == 1:
        x = g(x)
        y = g(g(y))
        d = math.gcd(abs(x - y), n)

    if d == n:
        if n_attempts > 0:
            return pollards_rho(n, n_attempts=n_attempts-1)
        else:
            return n
    else:
        return d


if __name__ == '__main__':
    import sys
    import timeit

    print(f'{wheel_factorization(224998304147131)}')