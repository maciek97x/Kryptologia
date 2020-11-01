#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re
import sys
import unidecode as ud
from random import choice
from string import ascii_lowercase

def open_file(filename):
    """
    Opens file and returns its content.

    Parameters:
        filename (string) - name of a file

    Returns:
        (string) file content

    Raises:
        TypeError: filename is not a string
    """
    if type(filename) != str:
        raise TypeError

    with open(filename, 'r') as f:
        content = f.read()

    return content

def clean_text(plaintext, keep_spaces=False):
    if type(plaintext) != str:
        raise TypeError

    if keep_spaces:
        pattern = r'[^a-zA-Zą-źĄ-Ź0-9 ]+'
    else:
        pattern = r'[^a-zA-Zą-źĄ-Ź0-9]+'

    return re.sub(pattern, '', plaintext)

def clean_num(plaintext):
    if type(plaintext) != str:
        raise TypeError

    return re.sub(r'[0-9]+', '', plaintext)

def clean_acc(plaintext, lower=True):
    if type(plaintext) != str:
        raise TypeError
    '''
    plaintext = plaintext.lower()
    sub_arr = [['ą', 'a'], ['ć', 'c'], ['ę', 'e'], ['ł', 'l'], ['ń', 'n'], ['ó', 'o'], ['ś', 's'], ['ż', 'z'], ['ź', 'z']]
    for p, s in sub_arr:
        plaintext = re.sub(p, s, plaintext)
    return plaintext
    '''
    if lower:
        plaintext = plaintext.lower()

    return ud.unidecode(plaintext)

def col_text(plaintext):
    if type(plaintext) != str:
        raise TypeError

    line_num = 0
    lines = []
    while line_num*35 < len(plaintext):
        line = plaintext[35*line_num:35*(line_num+1)]
        cols = [(line[5*col_num:len(line)], line[5*col_num:5*(col_num+1)])[(col_num + 1)*5 < len(line)] for col_num in range(7)]
        lines.append(' '.join(cols))
        line_num += 1
    return '\n'.join(lines)

def write_to_file(plaintext, filename):
    if type(plaintext) != str or type(filename) != str:
        raise TypeError

    with open(filename, 'w') as f:
        f.write(plaintext)
# ================ atbasz
def encrypt_atbasz(plaintext, *args, **kwargs):
    ciphertext = ''

    for a in plaintext:
        ciphertext += chr(25 - (ord(a) - ord('a')) + ord('a'))

    return ciphertext

decrypt_atbasz = encrypt_atbasz

# ================ rot13
def encrypt_rot13(plaintext, *args, **kwargs):
    ciphertext = ''

    for a in plaintext:
        ciphertext += chr((ord(a) - ord('a') + 13)%26 + ord('a'))

    return ciphertext

decrypt_rot13 = encrypt_rot13

# ================ cesar
def encrypt_cesar(plaintext, *args, **kwargs):
    ciphertext = ''

    for a in plaintext:
        ciphertext += chr((ord(a) - ord('a') + 3)%26 + ord('a'))

    return ciphertext

def decrypt_cesar(ciphertext, *args, **kwargs):
    plaintext = ''

    for a in ciphertext:
        plaintext += chr((ord(a) - ord('a') - 3)%26 + ord('a'))

    return plaintext

# ================ gaderypoluki
def encrypt_gaderypoluki(plaintext, *args, **kwargs):
    ciphertext = ''

    pairs = ('ga', 'de', 'ry', 'po', 'lu', 'ki')

    for a in plaintext:
        for pair in pairs:
            if a in pair:
                ciphertext += pair[a == pair[0]]
                break
        else:
            ciphertext += a

    return ciphertext

decrypt_gaderypoluki = encrypt_gaderypoluki

# ================ viganere
def encrypt_viganere(plaintext, key, *args, **kwargs):
    ciphertext = ''

    for i in range(len(plaintext)):
        ciphertext += chr(((ord(plaintext[i]) - ord('a')) + (ord(key[i%len(key)]) - ord('a')))%26 + ord('a'))

    return ciphertext

def decrypt_viganere(plaintext, key, *args, **kwargs):
    ciphertext = ''

    for i in range(len(plaintext)):
        ciphertext += chr(((ord(plaintext[i]) - ord('a')) - (ord(key[i%len(key)]) - ord('a')))%26 + ord('a'))

    return ciphertext

# ================ keygen
def keygen(output_file):
    with open(output_file, 'w') as file:
        for _ in range(26):
            file.write(choice(ascii_lowercase))

input_file = None
output_file = None
key_file = None
mode = None

available_mode = ('encrypt_atbasz', 'decrypt_atbasz',
                  'encrypt_viganere', 'decrypt_viganere',
                  'encrypt_rot13', 'decrypt_rot13',
                  'encrypt_cesar', 'decrypt_cesar',
                  'encrypt_gaderypoluki', 'decrypt_gaderypoluki')
key_required = ('encrypt_viganere', 'decrypt_viganere')

easy_mode = False

if len(sys.argv) < 2:
    print('Użycie:')
    print('./lab2.py -f <plik wejściowy> -o <plik wyjściowy> --mode <tryb (de)szyfrowania> [--key_file <plik z kluczem>]')
    print('./lab2.py --easy_mode')
    print('Wpisz ./lab2.py -h aby uzyskać więcej informacji')
    sys.exit()

elif sys.argv[1] in ('-h', '--help'):
    try:
        print(open('lab2_manual.txt').read())
    except:
        print('Brak pliku z manualem')
    sys.exit()

elif sys.argv[1] == '--easy_mode':
    easy_mode = True

elif len(sys.argv) > 2 and sys.argv[1] == '--keygen':
    keygen(sys.argv[2])
    sys.exit()

i = 0
while i < len(sys.argv):
    if sys.argv[i] in ('-f', '--file') and i + 1 < len(sys.argv):
        input_file = sys.argv[i+1]
        i += 1
    if sys.argv[i] in ('-o', '--output') and i + 1 < len(sys.argv):
        output_file = sys.argv[i+1]
        i += 1
    if sys.argv[i] in ('-k', '--key_file') and i + 1 < len(sys.argv):
        key_file = sys.argv[i+1]
        i += 1
    if sys.argv[i] in ('-m', '--mode') and i + 1 < len(sys.argv):
        mode = sys.argv[i+1]
        i += 1
    i += 1

input_file_loaded = False
easy_mode_b = True
while not input_file_loaded:
    try:
        if easy_mode and easy_mode_b:
            raise Exception
        print(f'Otwieranie pliku {input_file}... ', end='')
        plaintext = open_file(input_file)
        print('gotowe')
        input_file_loaded = True
    except:
        if not easy_mode_b:
            print('wystąpił błąd')
        easy_mode_b = False
        print('Podaj nazwę pliku wejściowego (exit aby wyjść)')
        input_file = input()
        if 'exit' == input_file.lower():
            sys.exit()

print(f'Szyfrowanie... ')

mode_selected = False
easy_mode_b = True
while not mode_selected:
    try:
        if easy_mode and easy_mode_b:
            raise Exception
        if mode not in available_mode:
            raise ValueError
        mode_selected = True
    except:
        if not easy_mode_b:
            print('Błąd. Wybrany tryb nie jest dostępny')
            print(f'Wybrany tryb: {mode}.')
        easy_mode_b = False
        print(f'Dostępne tryby: {available_mode}')
        print('Wybierz poprawny tryb (exit aby wyjść)')
        mode = input()
        if 'exit' == mode.lower():
            sys.exit()

key = None
if mode in key_required:
    key_file_loaded = False
    easy_mode_b = True
    while not key_file_loaded:
        try:
            if easy_mode and easy_mode_b:
                raise Exception
            print(f'Otwieranie pliku z kluczem {key_file}... ', end='')
            key = open_file(key_file)
            print('gotowe')
            key_file_loaded = True
        except:
            if not easy_mode_b:
                print('wystąpił błąd')
            easy_mode_b = False
            print('Podaj nazwę pliku z kluczem (exit aby wyjść)')
            key_file = input()
            if 'exit' == key_file.lower():
                sys.exit()

print('Usuwanie białych znaków... ', end='')
plaintext = clean_text(plaintext, False)
print('gotowe')
print('Usuwanie cyfr... ', end='')
plaintext = clean_num(plaintext)
print('gotowe')
print('Zamiana znaków diakrytycznych... ', end='')
plaintext = clean_acc(plaintext, True)
print('gotowe')

print('Właściwe szyfrowanie... ', end='')
ciphertext = locals()[mode](plaintext, key)
print('gotowe')

print('Zaszyfrowano')

output_file_opened = False
easy_mode_b = True
while not output_file_opened:
    try:
        if easy_mode and easy_mode_b:
            raise Exception
        print(f'Zapis wyniku do pliku {output_file}... ', end='')
        write_to_file(ciphertext, output_file)
        print('gotowe')
        output_file_opened = True
    except:
        if not easy_mode_b:
            print('wystąpił błąd')
        easy_mode_b = False
        print('Podaj nazwę pliku wyjściowego (exit aby wyjść)')
        output_file = input()
        if 'exit' == output_file.lower():
            sys.exit()
