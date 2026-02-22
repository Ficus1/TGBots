from random import randint
A = [randint(1, 20) for i in range(10)]
print(A)
print(min(A[:[i for i in range(len(A)) if A[i] % 2 == 0][0]] if A[0] % 2 != 0 else [0]))