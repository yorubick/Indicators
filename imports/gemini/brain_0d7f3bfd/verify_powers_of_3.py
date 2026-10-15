# Test if all transitions between unique C values are combinations of powers of 3 (1, 3, 9, 27)

unique_c = [15, 60, 62, 66, 67, 75, 77, 79, 80, 88, 106, 109, 110, 113, 115, 116, 118, 123, 134]

print("=== Successive Differences between Ordered Unique C values ===")
for i in range(len(unique_c) - 1):
    c1 = unique_c[i]
    c2 = unique_c[i+1]
    diff = c2 - c1
    # Check decomposition into powers of 3
    # 1, 3, 9, 27
    print(f"{c1:3d} -> {c2:3d} : diff = {diff:2d}")
