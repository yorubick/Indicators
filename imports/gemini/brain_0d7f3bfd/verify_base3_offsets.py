# Verification of the Base-3 Repunit Offset Formula
# offset(k) = (3^k - 1) // 2

def offset(k):
    return (3**k - 1) // 2

print("Powers of 3 sum formula (3^k - 1) / 2:")
for k in range(6):
    print(f"k={k}: offset = {offset(k):3d} -> C = 66 + {offset(k):3d} = {66 + offset(k):3d}")

# Compare with our exact measured values:
# At :45 (0 bars back from close of minute): k=0 -> offset=0  -> C=66
# At :30 (1 bar back from close of minute):  k=1 -> offset=1  -> C=67
# At :15 (2 bars back from close of minute):  k=3 -> offset=13 -> C=79
# At :00 (3 bars back from close of minute):  k=4 -> offset=40 -> C=106

measured = {
    '19:20:45': 66,
    '19:20:30': 67,
    '19:20:15': 79,
    '19:20:00': 106,
    '19:21:45': 66,
    '19:21:30': 79,
    '19:21:15': 106
}

print("\nComparison with empirical measurements:")
for t, c in measured.items():
    print(f"Time {t} | Measured C = {c:3d}")
