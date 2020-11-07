#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from random import randint
import sys
from time import perf_counter

class User(object):
    def __init__(self, p, g, x = None):
        self.p = p
        self.g = g
        if a is None:
            x = randint(2, p - 1)
        self.x = x
        self.g_to_x = None
        self.g_to_y = None
        self.g_to_xy = None

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

    print(' ', end='')
    for i in range(p - 1):
        print('\b' + '-\|/'[(i//1000)%4], end='')
        powers.append(potega_m(g, i, p))

    print('\b', end='')

    return len(set(powers)) == p - 1

def pdh(alice, bob):
    # sprawdzenie poprawnosci parametrow
    print('sprawdzanie poprawności parametrów... ', end='')
    assert alice.p == bob.p, 'Różne liczby pierwsze Alicji i Boba'
    assert alice.g == bob.g, 'Różne generatory Alicji i Boba'
    assert is_generator(p, g), 'Liczba g nie jest generatorem'
    print('ok')

    public_data = {}

    public_data['p'] = alice.p
    public_data['g'] = alice.g

    # obliczanie
    alice.g_to_x = potega_m(alice.g, alice.x, alice.p)
    bob.g_to_x = potega_m(bob.g, bob.x, bob.p)

    # wysłanie
    alice.g_to_y = bob.g_to_x
    bob.g_to_y = alice.g_to_x

    public_data['g_to_a'] = alice.g_to_x
    public_data['g_to_b'] = bob.g_to_x

    # obliczanie
    alice.g_to_xy = potega_m(alice.g_to_y, alice.x, alice.p)
    bob.g_to_xy = potega_m(bob.g_to_y, bob.x, alice.p)

    return public_data

def time_func(func):
    def time_func(*args, **kwargs):
        start = perf_counter()
        ret = func(*args, **kwargs)
        finish = perf_counter()
        return ret, finish - start

    return time_func

@time_func
def apdh_bruteforce(public_data):
    # wyciągamy dane dostępne publicznie
    p = public_data['p']
    g = public_data['g']
    g_to_a = public_data['g_to_a']
    g_to_b = public_data['g_to_b']

    print('Łamanie klucza...  ', end='')

    for k in range(p - 1):
        print('\b' + '-\|/'[(k//1000)%4], end='')

        power = potega_m(g, k, p)

        if power == g_to_a:
            print('\b ')
            return potega_m(g_to_b, k, p)

        if power == g_to_b:
            print('\b ')
            return potega_m(g_to_a, k, p)


def read_nums_from_file(num_count, message):
    filename = None
    done = False
    content = None
    nums = []

    while not done:
        if filename is not None and '.' not in filename:
            filename += '.txt'

        else:
            print(f'\n{message}')
            filename = input()
            if 'exit' == filename.lower():
                sys.exit()

        try:
            print(f'Otwieranie pliku {filename}... ', end='')
            with open(filename) as file:
                content = file.read()
                assert len(content.split()) >= num_count
                nums = list(map(int, content.split()[:num_count]))

            print('gotowe')
            done = True
        except:
            print('Wystąpił błąd przy otwieraniu pliku')
    return nums

p, g = read_nums_from_file(2, 'Podaj plik zawierający parametry p i g ' +\
                              '(exit aby wyjść)')

a = read_nums_from_file(1, 'Podaj plik zawierający tajną liczbę Alicji ' +\
                           '(exit aby wyjść)')[0]

b = read_nums_from_file(1, 'Podaj plik zawierający tajną liczbę Boba ' +\
                           '(exit aby wyjść)')[0]

print()

alice = User(p, g, a)
bob = User(p, g, b)

dh = pdh(alice, bob)

print(f'\nKlucz Alicji: {alice.g_to_xy}')
print(f'Klucz Boba: {bob.g_to_xy}')

print(f'\nPubliczne dane:')
for key, val in dh.items():
    print(f'\t{key} = {val}')
print()

key, time = apdh_bruteforce(dh)

print(f'Klucz o wartości {key} został złamany w czasie {time*1000:.3f} ms metodą bruteforce')
