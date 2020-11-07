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
    powers = []

    for i in range(p - 1):
        print('\r[' + '='*int(64*(i + 1)/(p - 1)) + ' '*(64 - int(64*(i + 1)/(p - 1))) + ']', end='')
        powers.append(potega_m(g, i, p))

    return len(set(powers)) == p - 1

while True:
    i = randint(2, p - 1)
    print('\n', i)
    if is_generator(p, i):
        print(' OK ')
