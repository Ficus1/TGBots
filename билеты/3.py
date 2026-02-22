from math import sin, radians
a, b, alpha = int(input()), int(input()), int(input())
S = 0.5 * a * b * sin(radians(alpha))
print(S)