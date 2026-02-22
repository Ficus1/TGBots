from random import randint
N, K = int(input()), int(input())
A = [randint(1, 10) for i in range(N)]
print(A)
print(sum([i for i in A if i % K == 0]))