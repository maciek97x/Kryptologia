#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from random import randint

p = int(sys.argv[1])

def potega_m(a, b, p):
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

def is_generator(p, g):
    prime_factors = []

    def gcd(a, b):
        while b != 0:
            a, b = b, a % b
        return a

    def get_factor(n):
        x_fixed = 2
        cycle_size = 2
        x = 2
        factor = 1

        while factor == 1:
            for count in range(cycle_size):
                if factor > 1: break
                x = (x * x + 1) % n
                factor = gcd(x - x_fixed, n)

            cycle_size *= 2
            x_fixed = x

        return factor

    q = p
    while q > 1:
        next = get_factor(q)
        prime_factors.append(next)
        q //= next

    powers = []

    for i in prime_factors:
        powers.append(potega_m(g, i, p))

    return 1 not in powers

while True:
    i = randint(2, p - 1)
    print('\n', i)
    if is_generator(p, i):
        print(' OK ')
