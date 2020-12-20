#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import numpy as np
from math import log2
from time import perf_counter
from msvcrt import getch
import traceback

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

def sr(p, q, seed):
    assert p != q, 'p and q should not be equal'
    assert len(seed) >= max(p, q), 'seed length should be greater or equal p and q'

    seed = np.array(seed, dtype=np.bool)

    new_seed = np.zeros_like(seed, dtype=np.bool)

    while True:
        new_seed[:-1] = seed[1:]

        new_seed[-1] = seed[-p] ^ seed[-q]      # xor

        seed = new_seed

        yield seed

def progress_bar(a, b):
    """
    Handles progress bar.
    Parameters:
        a (int)
        b (int)
    Returns:
        Progress bar consisting of [,= and ]             
    """
    return '[' + ('='*int(32*a/b)).ljust(32) + ']'

def rand(a, b, n, mode='lcg', progress=False, prefix=''):
    if a > b:
        raise ValueError
    if b - a + 1 > 2**31:
        raise ValueError

    if mode.lower() == 'lcg':
        gen = lcg(1103515245, 12345, 2**31, int(perf_counter()*(2**31))%(b-a))
        ret = []
        f = (2**31)//(b - a + 1)
        while len(ret) < n:
            if progress:
                print('\r' + prefix + progress_bar(len(ret), n), end='')
            num = next(gen)//f
            if num <= b - a + 1:
                ret.append(a + num)
        if progress:
            print('\r' + prefix + progress_bar(1, 1))
        return ret

    elif mode.lower() == 'lfsr':
        p = [1, 1, 0, 1, 1, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1]
        pc = perf_counter()
        gen = lfsr(p, [(int(pc*(2**32)) >> j) & 1 for j in range(len(p))])
        f = (2**31)//(b - a + 1)

        ret = []
        while len(ret) < n:
            if progress:
                print('\r' + prefix + progress_bar(len(ret), n), end='')
            num = 0
            for j in range(32):
                num += next(gen)[-1]*2**j
            num //= f
            if num <= b - a:
                ret.append(a + num)
        if progress:
            print('\r' + prefix + progress_bar(1, 1))
        return ret

    elif mode.lower() == 'sr':
        p, q = 3, 23
        pc = perf_counter()
        gen = sr(p, q, [(int(pc*(2**32)) >> j) & 1 for j in range(max(p, q))])
        f = (2**31)//(b - a + 1)

        ret = []
        while len(ret) < n:
            if progress:
                print('\r' + prefix + progress_bar(len(ret), n), end='')
            num = 0
            for j in range(32):
                num += next(gen)[-1]*2**j
            num //= f
            if num <= b - a:
                ret.append(a + num)
        if progress:
            print('\r' + prefix + progress_bar(1, 1))
        return ret

    else:
        print(f'Mode {mode} unsupported')
        return

def find_period(nums, progress=False, prefix=''):
    n = len(nums)
    for i in range(n - 1):
        if progress:
            print('\r' + prefix + progress_bar(i, n), end='')
        for j in range(i + 1, n):
            found = True
            for k in range(j, n, j - i):
                if nums[i:j] != nums[i+k:j+k]:
                    found = False
                    break
            if found:
                if progress:
                    print('\r' + prefix + progress_bar(1, 1))
                return j - i

    if progress:
        print('\r' + prefix + progress_bar(1, 1))
    return False

def generate_numbers(mode):
    os.system('cls' if os.name == 'nt' else 'clear')
    print(' GENEROWANIE '.center(64, '='))
    print()
    print( '  (ctrl+c - wyjście do menu)')
    print( '  Podaj parametry:')
    try:
        while True:
            a = input( '    min = ')
            if a.isnumeric():
                a = int(a)
                break
            else:
                print( '      Podano błędną wartość parametru min.')
        while True:
            b = input( '    max = ')
            if b.isnumeric() and int(b) >= a:
                b = int(b)
                break
            else:
                print( '      Podano błędną wartość parametru max.')
        while True:
            n = input( '    długość = ')
            if n.isnumeric():
                n = int(n)
                break
            else:
                print( '      Podano błędną wartość parametru długość.')
        print()
        print( '  Generowanie ciągu.')
        try:
            nums = rand(a, b, n, mode=mode, progress=True, prefix=' '*4)
        except:
            traceback.print_exc()
            return
        print( '    gotowe')
        print()
        print( '  Zapisywanie liczb do pliku.')
        while True:
            print( '  Nazwa pliku (default=nums.txt): ', end='')
            filename = input()
            try:
                if filename.strip() == '':
                    filename = 'nums.txt'
                with open(filename, 'w') as f:
                    for n in nums:
                        f.write(f'{n}\n')
                print(f'  Zapisano {len(nums)} liczb do pliku {filename}.')
                break
            except:
                pass
            print( '    Podaj właściwą nazwę pliku')
        print()
        print( '    Naciśnij enter aby powrócić do menu.', end='')
        input()
    except:
        print()
        print( '    Naciśnij enter aby powrócić do menu.', end='')
        input()
        return


def test_algorithms():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(' TEST OKRESOWOŚCI '.center(64, '='))
    print()
    print( '  (ctrl+c - wyjście do menu)')
    print( '  Podaj parametry testu:')
    try:
        while True:
            a = input( '    min = ')
            if a.isnumeric():
                a = int(a)
                break
            else:
                print( '      Podano błędną wartość parametru min.')
        while True:
            b = input( '    max = ')
            if b.isnumeric():
                b = int(b)
                break
            else:
                print( '      Podano błędną wartość parametru max.')
        while True:
            n = input( '    długość = ')
            if n.isnumeric():
                n = int(n)
                break
            else:
                print( '      Podano błędną wartość parametru długość.')
        print()
        for alg in algorithms:
            print(f'  Testowanie algorytmu {alg}.')
            print( '    Generowanie ciągu.')
            try:
                nums = rand(a, b, n, mode=alg, progress=True, prefix=' '*6)
            except:
                return

            print( '    Sprawdzanie okresowości (ctr+c - pomiń).')
            try:
                l = find_period(nums, progress=True, prefix=' '*6)
                if l > 0:
                    print(f'      Znaleziono okres długości {l}.')
                else:
                    print( '      Brak okresu.')
            except:
                print()
                print( '      Pominięto.')
            
            print( '    Sprawdzanie rozkładu.')
            hist = np.histogram(nums, bins=min(10, b - a + 1), range=(a, b + 1))
            print( '      Histogram:')
            for i in range(len(hist[0])):
                print(f'        [{hist[1][i]:.2f}, {hist[1][i+1]:.2f}{")]"[i == len(hist[0]) - 1]} : {hist[0][i]}')
            print()

        print()
        print('    Naciśnij enter aby powrócić do menu.', end='')
        input()
    except:
        return

algorithms = ('lcg', 'lfsr', 'sr')

os.system('cls' if os.name == 'nt' else 'clear')
print(' RNG '.center(64, '='))
print()
print(' '*16 + 'Autorzy:')
print(' '*18 + 'Katarzyna Wojewoda')
print(' '*18 + 'Maciej Torhan')
print()
print('  Naciśnij dowolny klawisz aby kontynuować.', end='', flush=True)

getch()

while True:
    c = None
    opt = 0
    while True:
        print(flush=True)
        os.system('cls' if os.name == 'nt' else 'clear')

        print(' MENU '.center(64, '='))
        print()
        print('  Wybierz akcję:')
        for i, alg in enumerate(algorithms):
            print(f'  {" >"[opt==i]} Generowanie liczb pseudolosowych algorytmem {alg}.')
        print(f'  {" >"[opt==len(algorithms)]} Testowanie algorytmów.')
        print(f'  {" >"[opt==len(algorithms)+1]} Wyjście.')

        c = ord(getch())
        if c == 224:
            c = ord(getch())

            if c == 80:
                opt += 1
                opt %= len(algorithms) + 2
            elif c == 72:
                opt -= 1
                opt %= len(algorithms) + 2
                
        elif c == 13:
            break

    if 0 <= opt < len(algorithms):
        generate_numbers(algorithms[opt])
    
    elif opt == len(algorithms):
        test_algorithms()
    
    elif opt == len(algorithms) + 1:
        print()
        print('    Zamykanie pogramu.\n')
        break