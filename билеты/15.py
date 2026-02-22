from random import randint
N = int(input())
A = [randint(0, 3) for i in range(N)]
print(A)
print(len([i for i in A if i == 0]))