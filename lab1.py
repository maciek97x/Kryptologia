import re

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

    return open(filename, 'r').read()

def remove_diacritics(plaintext):
    if type(plaintext) != str:
        raise TypeError

    sub_arr = [['ą', 'a'], ['ć', 'c'], ['ę', 'e'], ['ł', 'l'], ['ń', 'n'], ['ó', 'o'], ['ś', 's'], ['ż', 'z'], ['ź', 'z']]
    for p, s in sub_arr:
        plaintext = re.sub(p, s, plaintext)
    return plaintext

def leave_letters_only(plaintext):
    return re.sub(r'[^a-zA-Z]+', '', plaintext).lower()

