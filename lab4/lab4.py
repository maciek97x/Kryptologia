#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from time import perf_counter
from random import choice, randint
from getch import getch

# config
CIPHER_WIDTH = 4
MIN_P = 1 << (8*CIPHER_WIDTH//2)
MIN_Q = MIN_P
MAX_P = MIN_P << 2
MAX_Q = MAX_P

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
        g, y, x = euler_egcd(b % a, a)
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
    _, x, _ = euler_egcd(a, p)
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

def rand_prime(a, s):
    sieve = [True]*s
    primes = []

    sieve[0] = False
    sieve[1] = False

    i = 0
    for i in range(s):
        if 1 == sieve[i]:
            if i >= a:
                primes.append(i)
            for j in range(2*i, s, i):
                sieve[j] = 0
    
    return choice(primes)

def progress_bar(a, b):
    return '[' + ('='*int(32*a/b)).ljust(32) + ']'

@time_func
def is_prime_naive(p, progress=False, prefix=''):
    for i in range(2, int(p**.5)):
        if progress:
            print('\r' + prefix + progress_bar(i + 1, int(p**.5) - 2), end='')
        if 0 == p % i:
            if progress:
                print('\r' + prefix + progress_bar(1, 1))
            return False
    if progress:
        print('\r' + prefix + progress_bar(1, 1))
    return True

@time_func
def is_prime_fermat(p, s, progress=False, prefix=''):
    for i in range(s):
        if progress:
            print('\r' + prefix + progress_bar(i + 1, s), end='')
        t = randint(2, p-2)
        if power_mod(t, p - 1, p) != 1:
            if progress:
                print('\r' + prefix + progress_bar(1, 1))
            return False
    if progress:
        print('\r' + prefix + progress_bar(1, 1))
    return True

@time_func
def is_prime_mr(p, s, progress=False, prefix=''):
    u = 0
    r = p - 1
    while r & 1 == 0:
        r = r >> 1
        u += 1
    
    for i in range(s):
        if progress:
            print('\r' + prefix + progress_bar(i + 1, s), end='')
        t = randint(2, p-2)
        z = power_mod(t, r, p)
        if z != 1:
            j = 0
            while z != p - 1:
                z = power_mod(z, 2, p)
                if z == 1 or j == u:
                    if progress:
                        print('\r' + prefix + progress_bar(1, 1))
                    return False
                j += 1
    if progress:
        print('\r' + prefix + progress_bar(1, 1))
    return True

def calculate_keys():
    os.system('cls' if os.name == 'nt' else 'clear')

    print(' OBLICZANIE KLUCZY '.center(64, '='))
    print()
    
    print('  Kolejne obliczenia:')
    p = rand_prime(MIN_P, MAX_P)
    print(f'    p = {p}')
    q = rand_prime(MIN_Q, MAX_Q)
    print(f'    q = {q}')

    n = p*q
    print(f'    n = {n}')
    phi_n = (p - 1)*(q - 1)
    print(f'    Phi(n) = {phi_n}')

    while True:
        e = randint(2, phi_n - 1)
        if euler_gcd(e, phi_n) == 1:
            break
    print(f'    e = {e}')

    d = mod_inv(e, phi_n)
    print(f'    d = {d}')

    print()
    with open('public_key.txt', 'w') as f:
        f.write(f'{n} {e}')
    print(f'  Zapisano klucz publiczny ({n}, {e}) do pliku public_key.txt')

    with open('private_key.txt', 'w') as f:
        f.write(f'{p} {q} {d}')
    print(f'  Zapisano klucz prywatny ({p}, {q}, {d}) do pliku private_key.txt')

    print()
    print('    Naciśnij enter aby powrócić do menu.', end='')
    input()

def encrypt():
    os.system('cls' if os.name == 'nt' else 'clear')

    print(' SZYFROWANIE '.center(64, '='))
    print()
    
    while True:
        print('  Nazwa pliku (exit aby wrócić do menu): ', end='')
        filename = input()
        if filename.lower().strip() == 'exit':
            return
        try:
            plaintext = open(filename, 'r').read()
            print('    Poprawnie wczytano plik')
            break
        except:
            pass
        print('    Podaj właściwą nazwę pliku')

    print('  Wczytana wiadomość:')
    for i in range(min(4, len(plaintext)//32)):
        print(f'    {plaintext[i*32:min((i+1)*32, len(plaintext))]}')
    if len(plaintext)//32 > 4:
        print('    ...')

    print()
    print('  Wczytywanie pliku z kluczem publicznym...', end='')
    try:
        n, e = open('public_key.txt', 'r').read().split()
        n = int(n)
        e = int(e)
        print(' gotowe.')
    except:
        print(' wystąpił błąd')
        print('    Naciśnij enter aby powrócić do menu.', end='')
        input()
        return

    print(f'  Uzupełnienie wiadomości, aby jej długość była wielokrotnością {CIPHER_WIDTH}...', end='')
    while len(plaintext)%CIPHER_WIDTH != 0:
        plaintext += chr(randint(32, 255))
    print(' gotowe')
    
    ciphertext = bytearray()

    print('  Szyfrowanie...', end='')
    i = 0
    while i < len(plaintext):
        m = 0
        for j in range(CIPHER_WIDTH):
            m += ord(plaintext[i+j]) << (8*j)
        
        m = power_mod(m, e, n)
        print(f'{m:0x}')
        for j in range(CIPHER_WIDTH):
            ciphertext.append((m & (0xFF << (8*j))) >> (8*j))

        i += CIPHER_WIDTH
    print(' gotowe')
    for c in ciphertext:
        print(f'{c:0x}', end='')
    print(len(ciphertext))

    print()
    while True:
        print('  Nazwa pliku (exit aby wrócić do menu): ', end='')
        filename = input()
        if filename.lower().strip() == 'exit':
            return
        try:
            with open(filename, 'wb') as f:
                f.write(ciphertext)
            print('    Poprawnie zapisano wynik szyfrowania')
            break
        except:
            pass
        print('    Podaj właściwą nazwę pliku')

    print()
    print('    Naciśnij enter aby powrócić do menu.', end='')
    input()

def decrypt():
    os.system('cls' if os.name == 'nt' else 'clear')

    print(' DESZYFROWANIE '.center(64, '='))
    print()
    
    while True:
        print('  Nazwa pliku (exit aby wrócić do menu): ', end='')
        filename = input()
        if filename.lower().strip() == 'exit':
            return
        try:
            ciphertext = open(filename, 'rb').read()
            print('    Poprawnie wczytano plik')
            break
        except:
            pass
        print('    Podaj właściwą nazwę pliku')

    print()
    print('  Wczytywanie pliku z kluczem prywatnym...', end='')
    try:
        p, q, d = open('private_key.txt', 'r').read().split()
        p = int(p)
        q = int(q)
        d = int(d)
        print(' gotowe.')
    except:
        print(' wystąpił błąd')
        print('    Naciśnij enter aby powrócić do menu.', end='')
        input()
        return
    
    plaintext = ''

    print('  Deszyfrowanie...', end='')
    i = 0
    while i < len(ciphertext):
        m = 0
        for j in range(CIPHER_WIDTH):
            m += ciphertext[i+j] << (8*j)
        
        m = power_mod(m, d, p*q)

        for j in range(CIPHER_WIDTH):
            plaintext += chr((m & (0xFF << (8*j))) >> (8*j))

        i += CIPHER_WIDTH
    print(' gotowe')

    print('  Zdeszyfrowana wiadomość:')
    for i in range(min(4, len(plaintext)//32)):
        print(f'    {plaintext[i*32:min((i+1)*32, len(plaintext))]}')
    if len(plaintext)//32 > 4:
        print('    ...')
    print()

    print()
    while True:
        print('  Nazwa pliku (exit aby wrócić do menu): ', end='')
        filename = input()
        if filename.lower().strip() == 'exit':
            return
        try:
            with open(filename, 'w') as f:
                f.write(plaintext)
            print('    Poprawnie zapisano wynik deszyfrowania')
            break
        except:
            pass
        print('    Podaj właściwą nazwę pliku')

    print()
    print('    Naciśnij enter aby powrócić do menu.', end='')
    input()

def compare_tests():
    os.system('cls' if os.name == 'nt' else 'clear')

    print(' PORÓWNANIE TESTÓW '.center(64, '='))
    print()
    while True:
        print('  Liczba cyfr testowanych liczb (exit aby wrócić do menu): ', end='')
        digits = input()
        if digits.lower().strip() == 'exit':
            return
        if digits.isdecimal() and '.' not in digits:
            break
        print('    Podaj liczbę całkowitą')

    digits = int(digits)

    p = rand_prime(10**(digits - 1), 10**digits - 1)
    n = randint(10**(digits - 1), 10**digits - 1)
    n += n%2
    s = 100

    print('    Test 1...')
    test_1_p, time_1_p = is_prime_naive(p, progress=True, prefix=' '*6)
    test_1_n, time_1_n = is_prime_naive(n, progress=True, prefix=' '*6)
    
    print('    Test 2...')
    test_2_p, time_2_p = is_prime_fermat(p, s, progress=True, prefix=' '*6)
    test_2_n, time_2_n = is_prime_fermat(n, s, progress=True, prefix=' '*6)
    
    print('    Test 3...')
    test_3_p, time_3_p = is_prime_mr(p, s, progress=True, prefix=' '*6)
    test_3_n, time_3_n = is_prime_mr(n, s, progress=True, prefix=' '*6)

    print(f'  Liczba pierwsza: {p}')
    print( '    Wynik testów:')
    print( '      Algorytm naiwny:')
    print(f'        wynik: {test_1_p}')
    print(f'        czas:  {time_1_p}')
    print( '      Algorytm wykorzystujacy tw. Fermata:')
    print(f'        wynik: {test_2_p}')
    print(f'        czas:  {time_2_p}')
    print( '      Algorytm Millera-Rabina:')
    print(f'        wynik: {test_3_p}')
    print(f'        czas:  {time_3_p}')
    print( '    Porównanie')
    print(f'      ' + '='*int(32*time_1_p/max(time_1_p, time_2_p, time_3_p)))
    print(f'      ' + '='*int(32*time_2_p/max(time_1_p, time_2_p, time_3_p)))
    print(f'      ' + '='*int(32*time_3_p/max(time_1_p, time_2_p, time_3_p)))

    print(f'  Liczba: {n}')
    print( '    Wynik testów:')
    print( '      Algorytm naiwny:')
    print(f'        wynik: {test_1_n}')
    print(f'        czas:  {time_1_n}')
    print( '      Algorytm wykorzystujacy tw. Fermata:')
    print(f'        wynik: {test_2_n}')
    print(f'        czas:  {time_2_n}')
    print( '      Algorytm Millera-Rabina:')
    print(f'        wynik: {test_3_n}')
    print(f'        czas:  {time_3_n}')
    print( '    Porównanie')
    print( '      ' + '='*int(32*time_1_n/max(time_1_n, time_2_n, time_3_n)))
    print( '      ' + '='*int(32*time_2_n/max(time_1_n, time_2_n, time_3_n)))
    print( '      ' + '='*int(32*time_3_n/max(time_1_n, time_2_n, time_3_n)))

    print('    Naciśnij enter aby powrócić do menu.', end='')
    input()

os.system('cls' if os.name == 'nt' else 'clear')
print(' RSA '.center(64, '='))
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
        os.system('cls' if os.name == 'nt' else 'clear')

        print(' MENU '.center(64, '='))
        print()
        print('  Wybierz akcję:')
        print(f'  {" >"[opt==0]} Obliczanie kluczy i zapis do pliku.')
        print(f'  {" >"[opt==1]} Szyfrowanie wiadomości.')
        print(f'  {" >"[opt==2]} Deszyfrowanie wiadomości.')
        print(f'  {" >"[opt==3]} Porównanie testów pierwszości.')
        print(f'  {" >"[opt==4]} Wyjście.')

        c = getch()

        if ord(c) == 66:
            opt += 1
            opt %= 5
        elif ord(c) == 65:
            opt -= 1
            opt %= 5
        elif c == '\n':
            break

    if opt == 0:
        calculate_keys()
    
    elif opt == 1:
        encrypt()

    elif opt == 2:
        decrypt()
    
    elif opt == 3:
        compare_tests()
    
    elif opt == 4:
        print()
        print('    Zamykanie pogramu.\n')
        break