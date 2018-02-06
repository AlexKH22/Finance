import numpy as np
from binmodels import MultibinomialModel
from formulas import *

S0 = 100
r = 0.02
T = 0.25
sigma = 0.3
c = 0.01
n = 15

R, u, d, q = black_scholes_calibration(T, r, sigma, c, n)

print("Task 1")
model = MultibinomialModel(S0, u, d, R, n, q, euro=False, call=True, black=True)

K = 110
model.count_all_values(K)
print("Value is {}".format(round(model.C[0][0], 2)))

print()

print("Task 2")
model = MultibinomialModel(S0, u, d, R, n, q, euro=False, call=False, black=True)

K = 110
model.count_all_values(K)
print("Value is {}".format(round(model.C[0][0], 2)))

print()

print("Task 3")
print("Yes")
print()

print("Task 4")
for time, values in enumerate(zip(model.C, model.S)):
    for num in zip(values[0], values[1]):
        if num[0] == K-num[1]:
            print("At {} time there are such C: {} and K-S0: {}".format(time, num[0], K - num[1]))
            print("It is good to exercise")

print()

print("Task 5")
print("No")
print()

print("Task 6-7")
call = 1
amer_call = MultibinomialModel(S0, u, d, R, n, q, euro=False, call=True, black=True)

amer_call.count_all_values(K)
print("Stock lattice")

for time, values in enumerate(amer_call.S):
    print("At {} time there are such stock prices {}".format(time, values))

stocks = amer_call.S

print("Futures lattice")
futures_lattice = stocks[-1]
futures_lattice = [futures_lattice]

for i in range(len(futures_lattice[0])-1):
    futures_lattice.append([sum([q * futures_lattice[i][j] +
                                 (1-q) * futures_lattice[i][j+1]])
                            for j in range(len(futures_lattice[i])-1)])

futures_lattice = list(reversed(futures_lattice))

for time, values in enumerate(futures_lattice):
    print("At {} time there are such futures prices {}".format(time, values))

print("Option lattice")
option_lattice = [[max(call*(num-K), 0) for num in np.array(futures_lattice[10])]]
for i in range(len(option_lattice[0])-1):
    option_lattice.append([sum([1/R *
                                      (q * option_lattice[i][j] +
                                       (1-q) * option_lattice[i][j+1])])
                                 for j in range(len(option_lattice[i])-1)])

option_lattice = list(reversed(option_lattice))
for time, values in enumerate(option_lattice):
    print("At {} time there are such option prices {}".format(time, values))
print(round(option_lattice[0][0], 2))

i = 0
for f, o in zip(futures_lattice, option_lattice):
    print("t = {}".format(i))
    print([round(num, 2) for num in np.array(f) - K - np.array(o)])
    i += 1

print()

print("Task 8")
euro_call = MultibinomialModel(S0, u, d, R, n, q, euro=True, call=True, black=True)

K = 100
euro_call.count_all_values(K)
print("Euro call")
for time, values in enumerate(euro_call.C):
    print("At {} time there are such option prices {}".format(time, values))

euro_put = MultibinomialModel(S0, u, d, R, n, q, euro=True, call=False, black=True)

euro_put.count_all_values(K)
print("Euro put")

for time, values in enumerate(euro_put.C):
    print("At {} time there are such option prices {}".format(time, values))

top_6_call = euro_call.C[10][:6]
top_5_put = euro_put.C[10][6:]
futures_10 = top_6_call + top_5_put
C = [futures_10]

for i in range(len(C[0])-1):
    ls = []
    for j in range(len(C[i])-1):
        ls.append(sum([1/R *
                       (q * C[i][j] + (1-q) * C[i][j+1])]))
    C.append(ls)

chooser_lattice = list(reversed(C))
for time, values in enumerate(chooser_lattice):
    print("At {} time there are such chooser prices {}".format(time, values))
print(round(chooser_lattice[0][0], 2))
#
# # model.create_trading_strategies()
