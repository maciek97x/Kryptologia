#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from random import randint
import sys
from time import perf_counter

class User(object):
    """
    User class that represents endpoints of DH protocol
    """
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

def is_generator(p, g):
    """
    Checks if g is a primitive root modulo p. 
    Parameters:
        p (int) - prime number
        g (int)              
    """

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
        print('\r[' + '='*(int(64*(i + 1)/(p - 1))) + ' '*(64 - int(64*(i + 1)/(p - 1))) + ']', end='')
        powers.append(potega_m(g, i, p))
    print('\r[' + '='*64 + ']')

    print('\b', end='')

    return 1 not in powers

def pdh(alice, bob):
    """
    Follows Diffie–Hellman key exchange for two users
    Parameters:
        alice (User)
        bob (User)
    Returns:
        public data (ints) - p, g, g^a, g^b              
    """
    # sprawdzenie poprawnosci parametrow
    print('sprawdzanie poprawności parametrów... ')
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

@time_func
def apdh_bruteforce(public_data):
    """
    Attacks Diffie–Hellman with bruteforce attack
    Parameters:
        public data (ints) - p, g, g^a, g^b  
    Returns:
        Broken key (int)             
    """
    # wyciągamy dane dostępne publicznie
    p = public_data['p']
    g = public_data['g']
    g_to_a = public_data['g_to_a']
    g_to_b = public_data['g_to_b']

    print('Łamanie klucza...  ')

    for k in range(p - 1):
        print('\r[' + '='*(int(64*(k + 1)/(p - 1))) + ' '*(64 - int(64*(k + 1)/(p - 1))) + ']', end='')

        power = potega_m(g, k, p)

        if power == g_to_a:
            print('\r[' + '='*64 + ']')
            return potega_m(g_to_b, k, p)

        if power == g_to_b:
            print('\r[' + '='*64 + ']')
            return potega_m(g_to_a, k, p)

def euler_gcd(a, b):
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

@time_func
def apdh_babystep_giantstep(public_data):
    """
    Attacks Diffie–Hellman with Shanks method.
    Parameters:
        public data (ints) - p, g, g^a, g^b  
    Returns:
        Broken key (int)             
    """
    # wyciągamy dane dostępne publicznie
    p = public_data['p']
    g = public_data['g']
    g_to_a = public_data['g_to_a']
    g_to_b = public_data['g_to_b']

    print('Łamanie klucza...  ')

    p_sqrt_round = int(p**.5)

    baby_steps = []
    for i in range(p_sqrt_round - 1):
        print('\r[' + '='*(int(32*(i + 1)/(p - 1))) + ' '*(64 - int(32*(i + 1)/(p - 1))) + ']', end='')
        baby_steps.append(potega_m(g, i, p))

    g_inv = mod_inv(g, p)

    for i_a in range(p - 1):
        print('\r[' + '='*(32 + int(32*(i_a + 1)/(p - 1))) + ' '*(32 - int(32*(i_a + 1)/(p - 1))) + ']', end='')
        val = (g_to_a*potega_m(g_inv, i_a*int(p_sqrt_round), p)) % p
        if val in baby_steps:
            idx_a = baby_steps.index(val)
            break

    print('\r[' + '='*64 + ']')
    return potega_m(g_to_b, i_a*p_sqrt_round + idx_a, p)

def read_nums_from_file(num_count, message):
    """
    Opens file given number of times, returns numbers form file and prints messages for the use.
    Parameters:
        message (string) - message for the user
        num_count (int) - number of numbers in the file        
    Returns:
        numbers (int)             
    """
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

dh_public_data = pdh(alice, bob)

print(f'\nKlucz Alicji: {alice.g_to_xy}')
print(f'Klucz Boba: {bob.g_to_xy}')

print(f'\nPubliczne dane:')
for key, val in dh_public_data.items():
    print(f'\t{key} = {val}')
print()

key, time = apdh_bruteforce(dh_public_data)

print(f'Klucz o wartości {key} został złamany w czasie {time*1000:.3f} ms metodą bruteforce')

key, time = apdh_babystep_giantstep(dh_public_data)

print(f'Klucz o wartości {key} został złamany w czasie {time*1000:.3f} ms metodą baby-step giant-step')