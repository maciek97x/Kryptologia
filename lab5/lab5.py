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
        gen = lcg(69069, 1, b - a, int(perf_counter()*2**31)%(b-a))
        return [a + next(gen) for _ in range(n)]

    elif mode.lower() == 'lfsr':
        gen = lfsr([1, 0, 0, 1, 0, 1, 1, 1, 0, 0, 1],
                    [(int(perf_counter()*2**31) >> j) & 1 for j in range(11)])
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


print(rand(100, 10000, 20, 'lcg'))
print(rand(100, 10000, 20, 'lfsr'))