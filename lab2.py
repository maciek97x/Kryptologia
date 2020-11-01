#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re
import sys
import unidecode as ud

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

def encrypt_atbasz(plaintext, *args, **kwargs):
    ciphertext = ''

    for a in plaintext:
        ciphertext += chr(25 - (ord(a) - ord('a')) + ord('a'))

    return ciphertext

decrypt_atbasz = encrypt_atbasz

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

input_file = None
output_file = None
key_file = None
mode = None

available_mode = ('encrypt_atbasz', 'decrypt_atbasz', 'encrypt_viganere', 'decrypt_viganere')
key_required = ('encrypt_viganere', 'decrypt_viganere')

if len(sys.argv) < 2:
    print('Użycie: ./lab2.py -f <plik wejściowy> -o <plik wyjściowy> --mode <tryb (de)szyfrowania> [--key_file <plik z kluczem>]')
    print('Wpisz ./lab2.py -h aby uzyskać więcej informacji')

elif sys.argv[1] in ('-h', '--help'):
    try:
        print(open('lab2_manual.txt').read())
    except:
        print('Brak pliku z manualem')
    sys.exit()

i = 0
while i < len(sys.argv):
    if sys.argv[i] == '-f' and i + 1 < len(sys.argv):
        input_file = sys.argv[i+1]
        i += 1
    if sys.argv[i] == '-o' and i + 1 < len(sys.argv):
        output_file = sys.argv[i+1]
        i += 1
    if sys.argv[i] == '--key_file' and i + 1 < len(sys.argv):
        key = sys.argv[i+1]
        i += 1
    if sys.argv[i] == '--mode' and i + 1 < len(sys.argv):
        mode = sys.argv[i+1]
        i += 1
    i += 1

input_file_loaded = False
while not input_file_loaded:
    try:
        print(f'Otwieranie pliku {input_file}... ', end='')
        plaintext = open_file(input_file)
        print('gotowe')
        input_file_loaded = True
    except:
        print('wystąpił błąd')
        print('Podaj nazwę pliku jeszcze raz')
        input_file = input()
        if 'exit' == input_file.lower():
            sys.exit()

mode_selected = False
while mode_selected:
    try:
        print(f'Szyfrowanie ... ', end='')
        if mode not in available_mode:
            raise ValueError
    except:
        print('Błąd. Wybrany tryb nie jest dostępny')
        print(f'Dostępne tryby: {available_mode}')
        print(f'Wybrany tryb: {mode}.')
        print('Wybierz poprawny tryb')
        mode = input()
        if 'exit' == mode.lower():
            sys.exit()

key = None
if mode in key_required:
    key_file_loaded = False
    while not key_file_loaded:
        try:
            print(f'Otwieranie pliku z kluczem {key_file}... ', end='')
            key = open_file(key_file)
            print('gotowe')
            key_file_loaded = True
        except:
            print('wystąpił błąd')
            print('Podaj nazwę pliku jeszcze raz')
            key_file = input()
            if 'exit' == key_file.lower():
                sys.exit()

plaintext = clean_text(plaintext, False)
plaintext = clean_num(plaintext)
plaintext = clean_acc(plaintext, True)

ciphertext = locals()[mode](plaintext, key)

print('Zaszyfrowano')

output_file_opened = False
while not output_file_opened:
    try:
        print(f'Zapis wyniku do pliku {output_file}... ', end='')
        write_to_file(ciphertext, output_file)
        print('gotowe')
        output_file_opened = True
    except:
        print('wystąpił błąd.')
        print('Podaj nazwę pliku jeszcze raz')
        output_file = input()
        if 'exit' == output_file.lower():
            sys.exit()
