import os
from unidecode import unidecode as ud
from random import randint, seed
import io
from time import perf_counter
if os.name == 'nt':
    from msvcrt import getch
else:
    from getch import getch
import traceback

HASH_BYTES = 4
BLOCK_KEY = '1d5ee748'

def byte_to_bits(byte):
    """
    Converts bytes into bits
    Parameters:
        byte (int)
    Returns:
        bits (array(int))
    """
    return [int(b) for b in f'{byte:0b}']

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

def random_str(min_len, max_len):
    """
    Generate random string of lenght in given range.
    Handles progress bar.
    Parameters:
        min_len (int)
        max_len (int)
    Returns:
        ret (str)
    """
    l = randint(min_len, max_len)

    ret = ''

    for _ in range(l):
        ret += chr(randint(32, 127))
    
    return ret

def cmp_str(str_1, str_2):
    """
    Calculates percentage of matching characters in two strings.
    Parameters:
        min_len (int)
        max_len (int)
    Returns:
        percentage (int)
    """
    s = 0.
    for i in range(len(str_1)):
        s += int(str_1[i] == str_2[i])
    return s/len(str_1)

def hash_t(text):
    """
    Calculates hash for goven string.
    Parameters:
        text (str)
    Returns:
        hash (str)             
    """
    # zamiana znaków specjalnych na ascii
    text = ud(text)

    # 4 bajty - 8 znaków 0-9a-f
    n = 8*HASH_BYTES

    text_bits = []

    # zamiana tekstu na listę bitów i dodanie bitu parzystości
    for c in text:
        text_bits.extend(byte_to_bits(((ord(c) << 1 ) & 0xFE) | (f'{ord(c):0b}'.count('1') & 1)))

    # uzupełnienie bitów do odpowedniej długości
    seed(sum(text_bits))
    while len(text_bits) % n != 0:
        text_bits.append(randint(0, 1))
    
    # obliczanie xor'a
    ret = []
    for i in range(n):
        ret.append(sum(text_bits[i::n]) % 2)
    
    # zamiana 32 bitów na 4 bajty - 8 znaków 0-9a-f
    ret_hex = ''
    for i in range(len(ret)//8):
        ret_hex += f'{int("".join(map(str, ret[8*i:8*(i+1)])), 2):02x}'

    return ret_hex

def xor(bits_1, bits_2):
    """
    Exclusive or with given inputs.
    Parameters:
        bits_1 (array(int))
        bits_2 (array(int))
    Returns:
        xor (array(int))
    """
    ret = []

    for b_1, b_2 in zip(bits_1, bits_2):
        ret.append(b_1 ^ b_2)
    
    return ret

def block_t(text, key):
    """
    Calculates hash for goven string using block ciphers.
    Parameters:
        text (str)
    Returns:
        hash (str)             
    """
    # zamiana znaków specjalnych na ascii
    text = ud(text)

    text_bits = []

    # zamiana tekstu na listę bitów i dodanie bitu parzystości
    for c in text:
        text_bits.extend(byte_to_bits(((ord(c) << 1 ) & 0xFE) | (f'{ord(c):0b}'.count('1') & 1)))
    
    # zamiana klucza na bity
    key_bits = list(map(int, f'{int(key, 16):0b}'))
    while len(key_bits) % 8 != 0:
        key_bits.insert(0, 0)

    block_size = len(key_bits)

    # uzupełnienie bitów do odpowedniej długości
    seed(sum(text_bits))
    while len(text_bits) % block_size != 0:
        text_bits.append(randint(0, 1))
    
    # schemat Feistela
    for k in range(4):
        for n in range(len(text_bits)//block_size):
            block = text_bits[n*block_size:(n+1)*block_size]
            L_0 = block[:len(block)//2]
            R_0 = block[len(block)//2:]

            L_1 = R_0[:]
            R_1 = xor(L_0, xor(R_0, key_bits))
            text_bits[n*block_size:(n+1)*block_size] = L_1 + R_1
    
    ret = [0,]*len(key_bits)

    for n in range(len(text_bits)//block_size):
        ret = xor(ret, text_bits[n*block_size:(n+1)*block_size])

    # zamiana bitów na ciąg znaków 0-9a-f
    ret_hex = ''
    for i in range(len(ret)//8):
        ret_hex += f'{int("".join(map(str, ret[8*i:8*(i+1)])), 2):02x}'

    return ret_hex

def hash_file(filename, mode):
    """
    Reads text from given file and apply hash in given mode. 	
    Handles progress bar.
    Parameters:
        filename (str)
        mode (str)
    Returns:
        hashed text (array(str))
    """	
    with io.open(filename, 'r', encoding='utf8') as f:
        texts = f.readlines()
        print(f'    Wczytano {len(texts)} linii z pliku {filename}.')

    texts_hashes = []
    for i, text in enumerate(texts):
        if mode == 'hash':
            texts_hashes.append(hash_t(text))
        elif mode == 'block':
            texts_hashes.append(block_t(text, BLOCK_KEY))
        print('\r      ' + progress_bar(i, len(texts)), end='')
    print('\r      ' + progress_bar(1, 1))

    return texts_hashes

def hash_text(mode):
    """
    Prints messages for the user.
    Gets mode from the user.
    Gets files names form the user.
    Saves hashed text to file.
    Parameters:
        mode (str)
    """
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
        print('    Hashowanie...')
        texts_hashes = hash_file(filename, mode)
        print('      gotowe\n')
        print('  Zapisywanie wyniku do pliku.')
        while True:
            print( '  Nazwa pliku (default=hash.txt): ', end='')
            filename = input()
            try:
                if filename.strip() == '':
                    filename = 'hash.txt'
                with open(filename, 'w') as f:
                    for h in texts_hashes:
                        f.write(f'{h}\n')
                print(f'    Zapisano {len(texts_hashes)} hashy do pliku {filename}.')
                break
            except:
                pass
            print( '    Podaj właściwą nazwę pliku')
        print()
        print( '    Naciśnij enter aby powrócić do menu.', end='')
        input()
    except KeyboardInterrupt:
        print()
        print( '    Naciśnij enter aby powrócić do menu.', end='')
        input()
        return
    except:
        print('  Wystąpił błąd')
        print()
        traceback.print_exc()
        print()
        print( '    Naciśnij enter aby powrócić do menu.', end='')
        input()
        return

def test_algorithms():
    """    
    Prints messages for the user.
    Gets parameter from the user.
    Test algorithms.
    Prints results.
    Parameters:
        None
    """
    os.system('cls' if os.name == 'nt' else 'clear')
    print(' HASH '.center(64, '='))
    print()
    print( '  (ctrl+c - wyjście do menu)')
    try:
        while True:
            repeats = input( '  Liczba powtórzeń = ')
            if repeats.isnumeric():
                repeats = int(repeats)
                break
            else:
                print( '    Podano błędną wartość.')

        rand_texts = [random_str(8, 64) for _ in range(repeats)]
        print( '  1. Test bezkolizyjności')
        texts_hashes_1 = []
        texts_hashes_2 = []

        time_0 = perf_counter()
        for i in range(repeats):
            print('\r    ' + progress_bar(i//2, repeats), end='')

            texts_hashes_1.append(hash_t(rand_texts[i]))

        time_1 = perf_counter()
        for i in range(repeats):
            print('\r    ' + progress_bar(i//2 + repeats//2, repeats), end='')

            texts_hashes_2.append(block_t(rand_texts[i], BLOCK_KEY))

        time_2 = perf_counter()

        print('\r    ' + progress_bar(i, repeats))

        print(f'    Liczba wyrazów: {len(rand_texts)}')
        print( '    Liczba otrzymaych hashy (różnych):')
        print(f'      zwykłą metodą:    {len(set(texts_hashes_1))}')
        print(f'      szyfrem blokowym: {len(set(texts_hashes_2))}')
        print()
        print( '  2. Test wrażliwości na zmiany')
        result_1 = 0
        result_2 = 0
        for i in range(repeats):
            print('\r    ' + progress_bar(i, repeats), end='')
            text = random_str(8, 128)

            text_hash_1a = hash_t(text)
            text_hash_2a = block_t(text, BLOCK_KEY)

            # zmiana jednego znaku
            i = randint(0, len(text) - 1)
            s = random_str(1, 1)
            while s != text[i]:
                # w razie gdyby wylosowano ten sam
                s = random_str(1, 1)

            text = text[:i] + s + text[i+1:]

            text_hash_1b = hash_t(text)
            text_hash_2b = block_t(text, BLOCK_KEY)

            result_1 += cmp_str(text_hash_1a, text_hash_1b)
            result_2 += cmp_str(text_hash_2a, text_hash_2b)
        
        print('\r    ' + progress_bar(1, 1))

        result_1 /= repeats
        result_2 /= repeats

        print( '    Wyniki:')
        print(f'      zwykła metoda: {result_1}')
        print(f'      szyfr blokowy: {result_2}')
        print()
        print( '  3. Test szybkości')
        print( '    Wyniki:')
        print(f'      zwykła metoda: {1000*(time_1 - time_0)/repeats} ms')
        print(f'      szyfr blokowy: {1000*(time_2 - time_1)/repeats} ms')

        print()
        print( '    Naciśnij enter aby powrócić do menu.', end='')
        input() 
    except KeyboardInterrupt:
        print()
        print( '    Naciśnij enter aby powrócić do menu.', end='')
        input()
        return
    except:
        print('  Wystąpił błąd')
        print()
        traceback.print_exc()
        print()
        print( '    Naciśnij enter aby powrócić do menu.', end='')
        input()
        return


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

        if os.name == 'nt':
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
        else:
            c = ord(getch())
            if c == 27:
                c = ord(getch())
                if c == 91:
                    c = ord(getch())

                    if c == 66:
                        opt += 1
                        opt %= 4
                    elif c == 65:
                        opt -= 1
                        opt %= 4
            elif c == 10:
                break

    if opt == 0:
        hash_text('hash')

    elif opt == 1:
        hash_text('block')
    
    elif opt == 2:
        test_algorithms()
    
    elif opt == 3:
        print()
        print('    Zamykanie pogramu.\n')
        break
