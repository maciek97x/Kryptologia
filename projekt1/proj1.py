#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re
import sys
import os
import io
from unidecode import unidecode as ud
from msvcrt import getch
from random import choice
from string import ascii_lowercase

def encrypt_viganere(plaintext, key):
    """
    Encrypts plaintext using viganere algorithm.
    Parameters:
        plaintext (string) - file content
        key (string) - cipher key
    Returns:
        ciphered text (string)
    Raises:
        TypeError: plaintext is not a string
    """
    if type(plaintext) != str:
        return TypeError

    ciphertext = ''

    for i in range(len(plaintext)):
        ciphertext += chr(((ord(plaintext[i]) - ord('a')) + (ord(key[i%len(key)]) - ord('a')))%26 + ord('a'))

    return ciphertext

def decrypt_viganere(plaintext, key):
    """
    Decrypts plaintext using viganere algorithm.
    Parameters:
        plaintext (string) - file content
        key (string) - cipher key
    Returns:
        ciphered text (string)
    Raises:
        TypeError: plaintext is not a string
    """
    if type(plaintext) != str:
        raise TypeError

    ciphertext = ''

    for i in range(len(plaintext)):
        ciphertext += chr(((ord(plaintext[i]) - ord('a')) - (ord(key[i%len(key)]) - ord('a')))%26 + ord('a'))

    return ciphertext

def keygen(length):
    """
    Generates and saves to file random cipher key of given length
    Parameters
        length (int) - cipher key length
    Raises:
        TypeError: output_file is not a string or length is not a int
        ValueError: length is not positive
    """
    if length <= 0:
        raise ValueError

    key = ''
    for _ in range(length):
        key += choice(ascii_lowercase)
    
    return key

def encrypt():
    """
    Encrypts given message.
    Prints messages for the user.
    Gets files names form the user   
    Saves encrypted message to file.                       
    """
    os.system('cls' if os.name == 'nt' else 'clear')

    print(' SZYFROWANIE '.center(64, '='))
    print()
    
    while True:
        print('  Nazwa pliku (exit - wyjście): ', end='')
        filename = input()
        if filename.lower().strip() == 'exit':
            return
        try:
            plaintext = io.open(filename, 'r', encoding='utf8').read()
            print('    Poprawnie wczytano plik')
            break
        except:
            try:
                filename += '.txt'
                plaintext = io.open(filename, 'r', encoding='utf8').read()
                print('    Poprawnie wczytano plik')
                break
            except:
                pass
        print('    Podaj właściwą nazwę pliku')
    
    in_filename = filename
    plaintext = ud(plaintext)
    for c in ' \r\n\t':
        plaintext = plaintext.replace(c, '')

    print('  Wczytana wiadomość:', end='')
    for i in range(min(128, len(plaintext))):
        if i%32 == 0:
            print('\n    ', end='')
        print(plaintext[i], end='')

    if len(plaintext) > 128:
        print('...')
    else:
        print()

    print()
    print('  Wczytywanie pliku z kluczem.')

    while True:
        print('  Nazwa pliku (exit - wyjście, default=key.txt): ', end='')
        filename = input()
        if filename.lower().strip() == 'exit':
            return
        try:
            if filename.strip() == '':
                filename = 'key.txt'
            key = open(filename, 'r').read().strip()
            print(f'    Poprawnie wczytano klucz {key} z pliku {filename}.')
            break
        except:
            try:
                filename += '.txt'
                key = open(filename, 'r').read().strip()
                print(f'    Poprawnie wczytano klucz {key} z pliku {filename}.')
                break
            except:
                pass
        print('    Podaj właściwą nazwę pliku')

    print('  Szyfrowanie...', end='')
    ciphertext = encrypt_viganere(plaintext, key)
    print(' gotowe')

    print('  Zaszyfrowana wiadomość:', end='')
    for i in range(min(128, len(ciphertext))):
        if i%32 == 0:
            print('\n    ', end='')
        print(ciphertext[i], end='')

    if len(ciphertext) > 128:
        print('...')
    else:
        print()

    print()
    while True:
        print(f'  Nazwa pliku (exit - wyjście, default=enc_{in_filename}): ', end='')
        filename = input()
        if filename.lower().strip() == 'exit':
            return
        try:
            if filename.strip() == '':
                filename = f'enc_{in_filename}'
            with open(filename, 'w') as f:
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
    """
    Decrypts given message.
    Prints messages for the user.
    Gets files names form the user   
    Saves decrypted message to file.                       
    """
    os.system('cls' if os.name == 'nt' else 'clear')

    print(' DESZYFROWANIE '.center(64, '='))
    print()
    
    while True:
        print('  Nazwa pliku (exit - wyjście): ', end='')
        filename = input()
        if filename.lower().strip() == 'exit':
            return
        try:
            ciphertext = io.open(filename, 'r', encoding='utf8').read()
            print('    Poprawnie wczytano plik')
            break
        except:
            try:
                filename += '.txt'
                ciphertext = io.open(filename, 'r', encoding='utf8').read()
                print('    Poprawnie wczytano plik')
                break
            except:
                pass
        print('    Podaj właściwą nazwę pliku')
    
    in_filename = filename
    ciphertext = ud(ciphertext)

    print('  Wczytana wiadomość:', end='')
    for i in range(min(128, len(ciphertext))):
        if i%32 == 0:
            print('\n    ', end='')
        print(ciphertext[i], end='')

    if len(ciphertext) > 128:
        print('...')
    else:
        print()

    print()
    print('  Wczytywanie pliku z kluczem.')

    while True:
        print('  Nazwa pliku (exit - wyjście, default=key.txt): ', end='')
        filename = input()
        if filename.lower().strip() == 'exit':
            return
        try:
            if filename.strip() == '':
                filename = 'key.txt'
            key = open(filename, 'r').read().strip()
            print(f'    Poprawnie wczytano klucz {key} z pliku {filename}.')
            break
        except:
            try:
                filename += '.txt'
                key = open(filename, 'r').read().strip()
                print(f'    Poprawnie wczytano klucz {key} z pliku {filename}.')
                break
            except:
                pass
        print('    Podaj właściwą nazwę pliku')

    print('  Szyfrowanie...', end='')
    plaintext = decrypt_viganere(ciphertext, key)
    print(' gotowe')

    print('  Zdeszyfrowana wiadomość:', end='')
    for i in range(min(128, len(plaintext))):
        if i%32 == 0:
            print('\n    ', end='')
        print(plaintext[i], end='')

    if len(plaintext) > 128:
        print('...')
    else:
        print()

    print()
    while True:
        print(f'  Nazwa pliku (exit - wyjście, default=dec_{in_filename}): ', end='')
        filename = input()
        if filename.lower().strip() == 'exit':
            return
        try:
            if filename.strip() == '':
                filename = f'dec_{in_filename}'
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

def generate_key():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(' GENEROWANIE KLUCZA '.center(64, '='))
    print()
    print( '  Podaj długość klucza:')
    while True:
        l = input( '    l = ')
        if l.isnumeric() and int(l) > 0:
            l = int(l)
            break
        else:
            print( '      Podano błędną wartość.')

    print( '  Generoawnie klucza...', end='')
    key = keygen(l)
    print(' gotowe')
    print( '  Wygenerowany klucz:')
    print(f'    {key}')
    
    print()
    while True:
        print('  Nazwa pliku (exit - wyjście, default=key.txt): ', end='')
        filename = input()
        if filename.lower().strip() == 'exit':
            return
        try:
            if filename.strip() == '':
                filename = 'key.txt'
            with open(filename, 'w') as f:
                f.write(key)
            print('    Poprawnie zapisano klucz')
            break
        except:
            pass
        print('    Podaj właściwą nazwę pliku')

    print()
    print('    Naciśnij enter aby powrócić do menu.', end='')
    input()


os.system('cls' if os.name == 'nt' else 'clear')
print(' VIGANERE '.center(64, '='))
print()
print(' '*16 + 'Autorzy:')
print(' '*18 + 'Katarzyna Wojewoda')
print(' '*18 + 'Maciej Torhan')
print()
print('  Naciśnij dowolny klawisz aby kontynuować.', end='', flush=True)

options = (
    ('Szyfrowanie pliku pliku szyfrem Viganere', encrypt),
    ('Deszyfrowanie pliku pliku szyfrem Viganere', decrypt),
    ('Generowanie klucza', generate_key)
)

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
        for i, (option, _) in enumerate(options):
            print(f'  {" >"[opt==i]} {option}.')
        print(f'  {" >"[opt==len(options)]} Wyjście.')

        c = ord(getch())
        if c == 224:
            c = ord(getch())

            if c == 80:
                opt += 1
                opt %= len(options) + 1
            elif c == 72:
                opt -= 1
                opt %= len(options) + 1
                
        elif c == 13:
            break

    for i, (_, fun) in enumerate(options):
        if opt == i:
            fun()
    
    if opt == len(options):
        print()
        print('    Zamykanie pogramu.\n')
        break