import os
from unidecode import unidecode as ud
from random import randint, seed
import io
from time import perf_counter
from msvcrt import getch

def byte_to_bits(byte):
    return [int(b) for b in f'{byte:0b}']

def hash_line(text):
    text = ud(text)

    n = 8

    text_bits = []

    for c in text:
        text_bits.extend(byte_to_bits(((ord(c) << 1 ) & 0xFE) | (f'{ord(c):0b}'.count('1') & 1)))

    seed(sum(text_bits))
    while len(text_bits) % n != 0:
        text_bits.append(randint(0, 1))
    
    
    ret = []
    for i in range(n):
        ret.append(sum(text_bits[i::n]) % 2)
    
    while len(ret) % 8 != 0:
        ret.insert(0, 0)
    
    ret_hex = ''
    for i in range(len(ret)//8):
        ret_hex += f'{int("".join(map(str, ret[8*i:8*(i+1)])), 2):02x}'

    return ret_hex

def hash_t(filename):
    with open(filename, 'r') as f:
        texts = f.readlines()

    texts_hashes = []
    for i, text in enumerate(texts):
        texts_hashes.append(hash_line(text))
        print('\r' + progress_bar(i, len(texts)), end='')
    print('\r' + progress_bar(1, 1))

    return texts_hashes

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

def hash_text():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(' HASH '.center(64, '='))
    print()
    print( '  (ctrl+c - wyjście do menu)')
    try:
        while True:
            print( '  Nazwa pliku (default=text.txt): ', end='')
            filename = input()
            if filename.strip() == '':
                filename = 'text.txt'
            if os.path.isfile(filename):
                break
            filename += '.txt'
            if os.path.isfile(filename):
                break
            print( '    Podaj właściwą nazwę pliku')
        print()
        print('Hashowanie...')
        texts_hashes = hash_t(filename)
        print('gotowe')
        print( '  Zapisywanie wyniku do pliku.')
        while True:
            print( '  Nazwa pliku (default=hash.txt): ', end='')
            filename = input()
            try:
                if filename.strip() == '':
                    filename = 'hash.txt'
                with open(filename, 'w') as f:
                    for h in texts_hashes:
                        f.write(f'{h}\n')
                print(f'  Zapisano {len(texts_hashes)} hashy do pliku {filename}.')
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

def block_cipher_hash_text():
    pass

def test_algorithms():
    pass

os.system('cls' if os.name == 'nt' else 'clear')
print(' HASH '.center(64, '='))
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
        print(f'  {" >"[opt==0]} Hashowanie tekstu.')
        print(f'  {" >"[opt==1]} Hashowanie tekstu za pomocą szyfru blokowego.')
        print(f'  {" >"[opt==2]} Testowanie algorytmów.')
        print(f'  {" >"[opt==3]} Wyjście.')

        c = ord(getch())
        if c == 224:
            c = ord(getch())

            if c == 80:
                opt += 1
                opt %= 4
            elif c == 72:
                opt -= 1
                opt %= 4
                
        elif c == 13:
            break

    if opt == 0:
        hash_text()

    elif opt == 1:
        block_cipher_hash_text()
    
    elif opt == 2:
        test_algorithms()
    
    elif opt == 3:
        print()
        print('    Zamykanie pogramu.\n')
        break
