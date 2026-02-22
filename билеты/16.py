A = [1, 2, 3, 0, 4, 5, 6, 0, 0, 2, 3, 1, 0, 2]
print([i + 1 for i in range(len(A)) if A[i] == 0])