from math import factorial
n = int(input())
print(f"fact={'*'.join([str(i) for i in range(1, n + 1)])}={factorial(n)}")