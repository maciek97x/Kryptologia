from random import randint

class User(object):
    def __init__(self, p, g):
        self.p = p
        self.g = g
        self.a = randint(2, p - 1)
        self.g_to_a = None
        self.g_to_b = None
        self.g_to_ab = None

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

def pdh(alice, bob):
    public_data = {}

    public_data['p'] = alice.p
    public_data['g'] = alice.g

    # obliczanie
    alice.g_to_a = potega_m(alice.g, alice.a, alice.p)
    bob.g_to_a = potega_m(bob.g, bob.a, bob.p)

    # wysłanie
    alice.g_to_b = bob.g_to_a
    bob.g_to_b = alice.g_to_a

    public_data['alice_g_to_a'] = alice.g_to_a
    public_data['bob_g_to_a'] = bob.g_to_a

    # obliczanie
    alice.g_to_ab = potega_m(alice.g_to_b, alice.a, alice.p)
    bob.g_to_ab = potega_m(bob.g_to_b, bob.a, alice.p)

    return public_data

def apdh(public_data):
    p = public_data['p']
    g = public_data['g']
    g_to_a = public_data['alice_g_to_a']
    g_to_b = public_data['bob_g_to_a']


p = 7
g = 5

alice = User(p, g)
bob = User(p, g)

dh = pdh(alice, bob)

print(f'Klucz Alicji: {alice.g_to_ab}')
print(f'Klucz Boba: {bob.g_to_ab}')
print(f'Publicze dane: {dh}')
