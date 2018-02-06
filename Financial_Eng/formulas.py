import numpy as np
from itertools import product
from math import floor, sqrt, exp


def pres_value_per_year(payments, r, immediate=True):
    if immediate:
        s = [payments[k]/(1+r)**k for k in range(len(payments))]
        s = sum(s)
    else:
        s = [payments[k] / (1 + r) ** k for k in range(1, len(payments))]
        s = payments[0] + sum(s)
    s = round(s, 2)
    print("Present Value:", s)
    return s


def comp_int(money, r, n, quartely=False):
    if quartely:
        per_year = 4
        s = money * (1 + r/per_year) ** (per_year*n)
        print("Get {} after {} months".format(s, n))
    else:
        s = money*(1+r)**n
        print("Get {} after {} months".format(s, n))
    return s


def bound_perpetuity(A, r_lend, r_borrow):
    pv_borrow = A / r_borrow
    pv_lend = A / r_lend

    print("{} <= p <= {}".format(pv_borrow, pv_lend))
    return pv_borrow, pv_lend


def discount_rate(r, n, semi=False):
    if semi:
        d = 1 / (1 + r / 2) ** n
    else:
        d = 1 / (1 + r) ** n
    return d


def swap_int_rate(rates, years):
    num = 1 - discount_rate(rates[years-1], years)
    disc = [discount_rate(rates[i], i+1) for i in range(years)]
    den = sum(disc)

    return num/den


def futures_hedge_ratio(corr, needed_std, alt_std):
    cov = corr * needed_std * alt_std
    return cov/(needed_std*needed_std)


def options_binomial_model(S0, u, d, R, K, periods=1):
    S = [[]]*(periods+1)
    S[0] = [S0]
    changes = {
        'u': u,
        'd': d
    }

    for i in range(1, len(S)):
        S[i] = [0]*2**i
        j = 0
        changes_len = int(sqrt(len(S[i])))
        for p in product('ud' * changes_len, repeat=changes_len):
            for char in p:
                S[i][j] = S[i - 1][floor(j/2)] * changes[char]
                j += 1

    # Ax = b

    a = np.array([
        [S[1][0], R],
        [S[1][1], R]
    ])

    b = np.array([S[1][0]-K, 0])

    solution, resid, rank, s = np.linalg.lstsq(a, b)

    print("x: {}"
          "\ny: {}".format(round(solution[0], 3), round(solution[1], 3)))

    value = solution[0] * S0 + solution[1] * 1

    return value


def black_scholes_calibration(T, r, sigma, c, n):
    R = exp(r * T/n)
    u = exp(sigma * sqrt(T/n))
    d = 1/u
    q = (exp((r - c)*T/n) - d) / (u - d)

    return R, u, d, q
