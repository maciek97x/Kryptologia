from time import perf_counter

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