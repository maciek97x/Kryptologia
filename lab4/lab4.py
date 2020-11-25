from time import perf_counter
from random import choices

def power_mod(a, b, p):
    """
    Calculates a^b(mod p) in a faster way (O(log(n))).
    Parameters:
        a (int)
        b (int)
        p (int) - prime number
    Returns:
        calculated a^b(mod p) (int)             
    """
    if p == 1:
        return 0

    result = 1
    a = a % p
    while b > 0:
        if b & 1:
            result = (result * a) % p
        b = b >> 1
        a = (a * a) % p

    return result

def euler_gcd(a, b):
    while b:
        a, b = b, a%b
    return a

def euler_egcd(a, b):
    """
    Computes gcd using extended Euler algorithm
    Parameters:
        a (int) first number
        b (int) second number
    Returns:
        gcd of a and b (int)
    """
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = euler_gcd(b % a, a)
        return (g, x - (b // a) * y, y)

def mod_inv(a, p):
    
    """
    Computes multiplicative inverse modulo
    Parameters:
        a (int) number to be inverted
        p (int) prime number 
    Returns:
        inverse of a (int)            
    """
    g, x, y = euler_gcd(a, p)
    return x % p

def time_func(func):
    """
    Calculates how long does it take given function to perform.
    Parameters:
        func (function)
    Returns:
        func with elapsed time counter (function)           
    """
    def time_func(*args, **kwargs):
        start = perf_counter()
        ret = func(*args, **kwargs)
        finish = perf_counter()
        return ret, finish - start

    return time_func

def prime(a, s):
    sieve = [True]*s
    primes = []

    sieve[0] = False
    sieve[1] = False

    i = 0
    for i in range(s):
        if sieve[i] == 1:
            primes.append(i)
            for j in range(2*i, s, i):
                sieve[j] = 0
    
    return choices(primes, k=2)

def is_prime_1(p):
    raise NotImplementedError

def is_prime_2(p):
    raise NotImplementedError

def is_prime_3(p):
    raise NotImplementedError


print(prime(10, 1000))