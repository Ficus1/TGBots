from random import randint
from math import prod
A = [randint(-10, 10) for i in range(10)]
print(A)
print(prod([i for i in A if i < 0]))