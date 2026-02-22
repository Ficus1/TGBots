from random import randint
from math import prod
N = int(input())
A = [randint(-10, 10) for i in range(N)]
print(prod([i for i in A if i > 0]))