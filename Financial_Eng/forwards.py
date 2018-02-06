from formulas import *
from math import exp

S0 = 100
s = [0.1]
t = 30
n = 1000000

f_value = S0/discount_rate(s[0], t)
print(f_value)

f_value = S0/exp(-s[0] * t)
print(f_value)

value = S0*(1+s[0]/n)**(n*t)
print(value)

value = S0*exp(s[0])
print(value)