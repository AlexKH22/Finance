import formulas as f
import numpy as np

# Task 1
print("Task 1")

s = np.array([7.0, 7.3, 7.7, 8.1, 8.4, 8.8])
s *= 0.01
in_years = 4

print("Discount rate in {} years is {}".format(in_years, round(f.discount_rate(s[in_years-1], in_years), 3)))

# Task 2
print()
print("Task 2")
s = np.array([7.0, 7.3, 7.7, 8.1, 8.4, 8.8])
s *= 0.01
years = 6

print("Interest rate for {} years of a swap is {}%".format(years, round(100*f.swap_int_rate(s, years), 2)))

# Task 3
print()
print("Task 3")
print("Solution: 118.65")

# Task 4
print()
print("Task 4")
need_contracts = 10
orange_std = 0.2
grape_std = 0.25
corr = 0.7
hedge_ratio = f.futures_hedge_ratio(corr, orange_std, grape_std)
print("Optimal hedging ratio is {}".format(hedge_ratio))
print("Number of contracts to buy is {}".format(round(hedge_ratio*need_contracts, 0)))

# Task 5
print()
print("Task 5")
S0 = 100
u = 1.05
d = 1/u
R = 1.02
K = 102


print("The value of European call option on the stock with strike {} and given parameters"
      "\nS0 = {}"
      "\nu = {}"
      "\nd = {}"
      "\nR = {}"
      "\nis {}".format(K, S0, u, d, R, round(f.options_binomial_model(S0, u, d, R, K), 2)))

# Task 6
print()
print("Task 6")
print("Solution: y in Task 5")
