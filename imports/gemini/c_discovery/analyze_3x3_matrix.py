import numpy as np

# Matrix from C_MATRIZ_BORDES_RESULTADO.md
# Rows: START 18:54, 18:55, 18:56
# Cols: END 19:19, 19:20, 19:21
M = np.array([
    [134, 134, 109],
    [107,  62, 106],
    [ 77, 109, 134]
])

print("3x3 Matrix of C:")
print(M)

print("\nDifferences relative to central minimum C = 62:")
print(M - 62)

print("\nDifferences row-wise (step in END: 19:19 -> 19:20 -> 19:21):")
print(np.diff(M, axis=1))

print("\nDifferences col-wise (step in START: 18:54 -> 18:55 -> 18:56):")
print(np.diff(M, axis=0))
