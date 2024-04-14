import math


def eratosthenes(n: int) -> list[int]:
    '''
    Runs the sieve of Eratosthenes to find primes less than or equal to n.

    Parameters:
    n (int): upperbound for searching primes

    Returns:
    primes (list[int]): prime numbers less than or equal to n
    '''
    
    sieve = [True for _ in range(n+1)]
    sieve[0], sieve[1] = False, False

    i = 2
    while i ** 2 <= n:
        if sieve[i]:
            for j in range(i ** 2, n + 1, i):
                sieve[j] = False

        i += 1

    return [i for i, check in enumerate(sieve) if check]

