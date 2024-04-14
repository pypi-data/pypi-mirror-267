import math
import random


def _basic_check(n: int) -> bool:
    if type(n) != int:
        raise TypeError('n must be an integer')

    if n <= 0:
        raise ValueError('n must be a positive integer')
    elif n == 1:
        return False
    elif n <= 3:
        return True
    elif n % 2 == 0:
        return False

    return None


def fermat(n: int, k: int=100) -> bool:
    '''
    Performs Fermat Primality Test

    Parameters:
    n (int): Number to perform test on
    k (int): Number of rounds to perform tests

    Returns:
    result (bool): True for probable prime and False for composite
    '''
    if _basic_check(n) != None:
        return _basic_check(n)

    for _ in range(k):
        a = n
        while math.gcd(a, n) != 1:
            a = random.randint(2, n - 2)

        if pow(a, n - 1, n) != 1:
            return False

    return True


def miller_rabin(n: int, k: int=100) -> bool:
    '''
    Performs Miller Rabin Primality Test

    Parameters:
    n (int): Number to perform test on
    k (int): Number of rounds to perform tests

    Returns:
    result (bool): True for probable prime and False for composite
    '''
    if _basic_check(n) != None:
        return _basic_check(n)

    s = 0
    d = n - 1

    while d % 2 == 0:
        s += 1
        d //= 2

    for _ in range(k):
        a = random.randint(2, n - 2)
        x = pow(a, d, n)

        for _ in range(s):
            y = pow(x, 2, n)

            if y == 1 and x != 1 and x != n - 1:
                return False

            x = y

        if y != 1:
            return False

    return True


def miller(n: int) -> bool:
    '''
    Performs Miller Primality Test (deterministic)

    Parameters:
    n (int): Number to perform test on

    Returns:
    result (bool): True for prime and False for composite
    '''
    if _basic_check(n) != None:
        return _basic_check(n)

    s = 0
    d = n - 1

    while d % 2 == 0:
        s += 1
        d //= 2

    # deterministic set of bases
    a_i = []
    if n < 2_047:
        a_i = [2]
    elif n < 1_373_653:
        a_i = [2, 3]
    elif n < 9_080_191:
        a_i = [31, 73]
    elif n < 25_326_001:
        a_i = [2, 3, 5]
    elif n < 3_215_031_751:
        a_i = [2, 3, 5, 7]
    elif n < 4_759_123_141:
        a_i = [2, 7, 61]
    elif n < 1_122_004_669_633:
        a_i = [2, 13, 23, 1662803]
    elif n < 2_152_302_898_747:
        a_i = [2, 3, 5, 7, 11]
    elif n < 3_474_749_660_383:
        a_i = [2, 3, 5, 7, 11, 13]
    elif n < 341_550_071_728_321:
        a_i = [2, 3, 5, 7, 11, 13, 17]
    elif n < 3_825_123_056_546_413_051:
        a_i = [2, 3, 5, 7, 11, 13, 17, 19, 23]
    elif n < 318_665_857_834_031_151_167_461:
        a_i = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37]
    elif n < 3_317_044_064_679_887_385_961_981:
        a_i = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41]
    else:
        a_i = range(2, int(2 * (math.log(n) ** 2)))

    for a in a_i:
        x = pow(a, d, n)

        for _ in range(s):
            y = pow(x, 2, n)

            if y == 1 and x != 1 and x != n - 1:
                return False

            x = y

        if y != 1:
            return False

    return True


if __name__ == '__main__':
    import sys

    print(f'prob: {miller_rabin_probabalistic(int(sys.argv[1]))}')
    print(f'det : {miller_rabin_deterministic(int(sys.argv[1]))}')
    print(f'ferm: {fermat_probabilistic(int(sys.argv[1]))}')
