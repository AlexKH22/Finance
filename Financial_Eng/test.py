from numpy import random, sum

N = int(raw_input('Number of experiments: '))
ndice = int(raw_input('Number of dice: '))
nsix = int(raw_input('Number of dice with six eyes: '))

eyes = random.random_integers(1, 6, (N, ndice))
compare = eyes == 6
nthrows_with_6 = sum(compare, axis=1)  # суммирование по столбцам - элементам строки (axis = 1)
nsuccesses = nthrows_with_6 >= nsix
M = sum(nsuccesses)
p = float(M)/N
print('probability:', p)