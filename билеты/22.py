from random import randint
A = [randint(-10, 10) for i in range(10)]
print(A)
print(len([i for i in A if i >= 0]))