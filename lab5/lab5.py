# -*- coding: utf-8 -*-
import numpy as np
from math import log2
from time import perf_counter

def lcg(a, b, M, seed):
    x = seed
    while True:
        x = (a*x + b)%M
        yield x

def lfsr(p, seed):
    assert len(p) == len(seed)

    p = np.array(p, dtype=np.bool)
    seed = np.array(seed, dtype=np.bool)

    new_seed = np.zeros_like(seed, dtype=np.bool)

    while True:
        new_seed[:-1] = seed[1:]

        new_seed[-1] = (p & seed).sum()%2

        seed = new_seed

        yield seed

def rand(a, b, n, mode='lcg'):
    if mode.lower() == 'lcg':
        gen = lcg(1103515245, 12345, 2**31, int(perf_counter()*(2**31))%(b-a))
        ret = []
        f = (2**31)//(b-a)
        while len(ret) < n:
            num = next(gen)//f
            if num <= b - a:
                ret.append(a + num)
        return ret

    elif mode.lower() == 'lfsr':
        p = [1, 1, 0, 1, 1, 0, 0, 1, 1, 0, 1, 1, 1, 1, 0, 1]
        gen = lfsr(p, [(int(perf_counter()*(2**31)) >> j) & 1 for j in range(len(p))])
        bits = int(log2(b - a) + 1./9)

        ret = []
        while len(ret) < n:
            num = 0
            for j in range(bits):
                num += next(gen)[-1]*2**j
            if num > b - a:
                continue
            ret.append(a + num)
        return ret

    else:
        print(f'Mode {mode} unsupported')
        return

# sprawdzenie jakości geenratorów - wyświetlone liczby powinny być mniej więcej równe
r1 = rand(100, 1000, 10000, 'lcg')
print(np.histogram(r1)[0])

r2 = rand(100, 1000, 10000, 'lfsr')
print(np.histogram(r2)[0])