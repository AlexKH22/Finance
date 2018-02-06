import formulas as f

# Task 1
print("Task 1")

payments = [500000]*20
r = 0.1
im = True

s = f.pres_value_per_year(payments, r, im)

# Task 2
# Option 1
# Deposit $1000
# Pay $1000 per month (6 months)
print()
print("Task 2")

per_month_1 = 1000
deposit_1 = 1000
r = 0.12
payments_1 = [per_month_1]*6
all_together_1 = sum(payments_1) + deposit_1

all_deposits_1 = f.comp_int(900, r, 6)
print("All earnings with deposits #1:", all_deposits_1)

# Option 1
# Deposit $1000
# Additional $900 deposit
# Pay $900 per month (6 months)

per_month_2 = 900
deposit_2 = 1000 + per_month_2
r = 0.12
payments_2 = [per_month_2]*6
all_together_2 = sum(payments_2) + deposit_2

all_deposits_2 = sum([f.comp_int(per_month_1-per_month_2, r, k) for k in range(1, 7)])
print("All earnings with deposits #2:", all_deposits_2)

print('Option 1: {} and Option 2: {}'.format(all_together_1-all_deposits_1, all_together_2-all_deposits_2))

# Task 3
print()
print("Task 3")

s1 = 0.063
s2 = 0.069

d = round(f.discount_rate(s2, 2), 3)

print("Discount rate {}".format(d))

# Task 4
print()
print("Task 4")

s1 = 0.063
s2 = 0.069

d = round(((1+s2)**2/(1+s1)**1 - 1) * 100, 1)

print("Forward rate {}%".format(d))

# Task 5
print()
print("Task 5")

A = 400
r = 0.08
months = 9

p = round(f.comp_int(A, r, months/12, quartely=True), 2)
print("Stock forward price {}".format(p))

# Task 6
# Perpetuity
print()
print("Task 6")

r_lend = 0.08
r_borrow = 0.1
A = 10000

pv_borrow, pv_lend = f.bound_perpetuity(A, r_lend, r_borrow)
print("Difference: {}".format(pv_lend - pv_borrow))

# Task 7
# Value of a Forward contract at an intermediate time
print()
print("Task 7")

S0 = 100
St = 125
r = 0.1

F0 = S0/f.discount_rate(r, 2, semi=True)
print('F0 = {}'.format(F0))

Ft = St/f.discount_rate(r, 1, semi=True)
print('Ft = {}'.format(Ft))

print("Forward contract value: {}".format(round((Ft-F0)*f.discount_rate(r, 1, semi=True), 1)))