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

def encrypt_atbasz(plaintext):
    ciphertext = ''

    for a in plaintext:
        ciphertext += chr(25 - (ord(a) - ord('a')) + ord('a'))

    return ciphertext

decrypt_atbasz = encrypt_atbasz

def encrypt_viganere(plaintext, key):
    ciphertext = ''

    for i in range(len(plaintext)):
        ciphertext += chr(((ord(plaintext[i]) - ord('a')) + (ord(key[i%len(key)]) - ord('a')))%26 + ord('a'))
    
    return ciphertext

def decrypt_vigenere(plaintext, key):
    ciphertext = ''

    for i in range(len(plaintext)):
        ciphertext += chr(((ord(plaintext[i]) - ord('a')) - (ord(key[i%len(key)]) - ord('a')))%26 + ord('a'))
    
    return ciphertext

input_file = None
output_file = None
key = None
mode = None

available_modes = ('encrypt_atbasz', 'decrypt_atbasz', 'encrypt_viganere', 'decrypt_viganere')

i = 0
while i < len(sys.argv):
    if sys.argv[i] == '-f' and i + 1 < len(sys.argv):
        input_file = sys.argv[i+1]
        i += 1
    if sys.argv[i] == '-o' and i + 1 < len(sys.argv):
        output_file = sys.argv[i+1]
        i += 1
    if sys.argv[i] == '--key' and i + 1 < len(sys.argv):
        key = sys.argv[i+1]
        i += 1
    if sys.argv[i] == '--mode' and i + 1 < len(sys.argv):
        mode = sys.argv[i+1]
        i += 1
    i += 1

done = False
while not done:
    try:
        print(f'Otwieranie pliku {input_file}... ', end='')
        plaintext = open_file(input_file)
        print('gotowe')

        print(f'Szyfrowanie ... ', end='')
        if mode not in available_modes:
            print(f'Błąd. Wybrany tryb nie jest dostępny.\nDostępne tryby: {available_modes}.\nWybrany tryb: {mode}.')
            raise ValueError
        plaintext = clean_text(plaintext, False)
        plaintext = clean_num(plaintext)
        plaintext = clean_acc(plaintext, True)
        if mode in  ('encrypt_atbasz', 'decrypt_atbasz'):
            ciphertext = locals()[mode](plaintext)
        elif mode in ('encrypt_viganere', 'decrypt_viganere'):
            if key is None:
                print('Brak klucza.')
                raise ValueError
            ciphertext = locals()[mode](plaintext, key)
        print('gotowe')

        print(f'Zapis wyniku do pliku {output_file}... ', end='')
        write_to_file(ciphertext, output_file)
        print('gotowe')

        done = True
    except:
        print('Wystąpił błąd. Podaj opcje jeszcze raz. Wpisane "exit" powoduje wyjście z programu')
        input_file = input('Plik wejściowy: ')
        if 'exit' == input_file.lower():
            sys.exit()
        output_file = input('Plik wyjściowy: ')
        if 'exit' == output_file.lower():
            sys.exit()
        mode = input(f'Tryb {available_modes}: ')
        if 'exit' == mode.lower():
            sys.exit()
        elif mode in ('encrypt_viganere', 'decrypt_viganere'):
            key = input('Klucz: ')
            if 'exit' == key.lower():
                sys.exit()