from random import randint
A = [randint(1, 10) for i in range(10)]
print(A)
print(max(A), A.index(max(A)))