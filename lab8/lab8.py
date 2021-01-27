import numpy as np
import matplotlib.pyplot as plt

def elip(a, b, pairs=[]):
    '''
    Funkcja rysująca krzywą eliptyczną, podane pary punktów (P, Q) na niej leżące, -P oraz P + Q.
    Parametry:
        a (int) - współczynnik a krzywej
        b (int) - współczynnik b krzywej
        pairs (list(tuple(int, int))) - lista par punktów
    '''
    # walidacja parametrów
    if 4*(a**3) + 27*(b**2) == 0:
        print('Błedne parametry.')
        return
    
    # parametry wykresu
    plot_r = 5
    n = 100

    # dziedzina, na której wyznaczamy krzywą
    x = np.linspace(-plot_r, plot_r, n)
    y = np.linspace(-plot_r, plot_r, n)

    x, y = np.meshgrid(x, y)

    # strony równania krzywej
    LHS = y**2
    RHS = x**3 + a*x + b

    # obliczamy sumy P + Q oraz -P
    pairs_sums_mp = []

    for p, q in pairs:
        # sprawdzenie czy punkt leży na krzywej (z pewną dokładnością)
        if np.abs(p[1]**2 - p[0]**3 - a*p[0] - b) < .01 and \
           np.abs(q[1]**2 - q[0]**3 - a*q[0] - b) < .01:
            s = (q[1] - p[1])/(q[0] - p[0])
            r_1 = s**2 - p[0] - q[0]
            r_2 = s*(p[0] - r_1) - p[1]
            m_p = (p[0], -p[1])
            pairs_sums_mp.append((p, q, (r_1, r_2), m_p))

    # tworzymy nowy rysunek
    plt.figure(figsize=(6, 6))

    # rysujemy krzywą
    plt.contour(x, y, (LHS - RHS), [0], color='C0')

    # dodajemy punkty i proste
    for i, (p, q, r, m_p) in enumerate(pairs_sums_mp):
        # proste
        plt.vlines(r[0], -plot_r, plot_r, linewidth=1)
        plt.axline(p, q, linewidth=1)

        # punkty
        plt.scatter(*p, s=16, color='C1', zorder=8)
        plt.scatter(*q, s=16, color='C3', zorder=8)
        plt.scatter(*r, s=16, color='C4', zorder=8)
        plt.scatter(*m_p, s=16, color='C2', zorder=8)
        plt.scatter(r[0] , -r[1], s=8, color='C4', zorder=8)

        # podpisy
        plt.text(*p, f' P_{i}', zorder=16)
        plt.text(*q, f' Q_{i}', zorder=16)
        plt.text(*r, f' R_{i}', zorder=16)
        plt.text(*m_p, f' -P_{i}', zorder=16)

    # granice wykresu
    plt.xlim(-plot_r, plot_r)
    plt.ylim(-plot_r, plot_r)

    # wyświetlenie rysunku
    plt.show()

elip(-2, 2, [((0., 2**.5), (-1.769, 0.)), ((-0.816, 1.757), (2., -2.449))])
