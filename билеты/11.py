from random import randint
b = int(input())
A = [randint(50, 200) for i in range(15)]
print(A)
print(sum([i for i in A if i < 100 and i % b == 0]))