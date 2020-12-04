#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from time import perf_counter
from random import choices, randint

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
        if 1 == sieve[i]:
            if i > a:
                primes.append(i)
            for j in range(2*i, s, i):
                sieve[j] = 0
    
    return choices(primes, k=2)

@time_func
def is_prime_naive(p):
    for i in range(2, int(p**.5)):
        if 0 == p % i:
            return False
    return True

@time_func
def is_prime_fermat(p, s):
    for _ in range(s):
        t = randint(2, p-2)
        if power_mod(t, p - 1, p) != 1:
            return False

    return True

@time_func
def is_prime_mr(p, s):
    u = 0
    r = p - 1
    while r & 1 == 0:
        r = r >> 1
        u += 1
    
    for _ in range(s):
        t = randint(2, p-2)
        z = power_mod(t, r, p)
        if z != 1:
            j = 0
            while z != p - 1:
                z = power_mod(z, 2, p)
                if z == 1 or j == u:
                    return False
                j += 1

    return True

digits = 7

for _ in range(1):
    p = prime(10**(digits - 1), 10**digits - 1)[0]
    n = randint(10**(digits - 1), 10**digits - 1)
    s = 1

    print('Test 1...')
    test_1_p, time_1_p = is_prime_naive(p)
    test_1_n, time_1_n = is_prime_naive(n)
    
    print('Test 2...')
    test_2_p, time_2_p = is_prime_fermat(p, s)
    test_2_n, time_2_n = is_prime_fermat(n, s)
    
    print('Test 3...')
    test_3_p, time_3_p = is_prime_mr(p, s)
    test_3_n, time_3_n = is_prime_mr(n, s)

    print(f'Liczba pierwsza: {p}')
    print('\tWynik testów:')
    print(f'\t\tAlgorytm naiwny:')
    print(f'\t\t\twynik: {test_1_p}')
    print(f'\t\t\tczas:  {time_1_p}')
    print(f'\t\tAlgorytm wykorzystujacy tw. Fermata:')
    print(f'\t\t\twynik: {test_2_p}')
    print(f'\t\t\tczas:  {time_2_p}')
    print(f'\t\tAlgorytm Millera-Rabina:')
    print(f'\t\t\twynik: {test_3_p}')
    print(f'\t\t\tczas:  {time_3_p}')
    
    print(f'Liczba: {n}')
    print('\tWynik testów:')
    print(f'\t\tAlgorytm naiwny:')
    print(f'\t\t\twynik: {test_1_n}')
    print(f'\t\t\tczas:  {time_1_n}')
    print(f'\t\tAlgorytm wykorzystujacy tw. Fermata:')
    print(f'\t\t\twynik: {test_2_n}')
    print(f'\t\t\tczas:  {time_2_n}')
    print(f'\t\tAlgorytm Millera-Rabina:')
    print(f'\t\t\twynik: {test_3_n}')
    print(f'\t\t\tczas:  {time_3_n}')