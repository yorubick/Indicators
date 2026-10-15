# Harmonic decomposition of C_15s and C_1m
# Base powers of 3: 3, 9, 27, 81

c_15s_vals = [88, 67, 88, 88, 79, 102, 123, 67, 87, 106, 87, 123, 87]
c_1m_vals = [50, 52, 71, 135, 130, 88, 135, 112, 136, 112, 112, 135, 112]

print("=== DIFFERENCES AMONG C_15s UNIQUE VALUES ===")
uniq_15s = sorted(list(set(c_15s_vals)))
print("Unique C_15s:", uniq_15s)
for i in range(len(uniq_15s)):
    for j in range(i+1, len(uniq_15s)):
        d = uniq_15s[j] - uniq_15s[i]
        print(f"{uniq_15s[j]} - {uniq_15s[i]} = {d} (d/9 = {d/9:.2f}, d/3 = {d/3:.2f})")

print("\n=== DIFFERENCES AMONG C_1m UNIQUE VALUES (Long regime n>=24) ===")
uniq_1m = sorted(list(set(c_1m_vals[3:])))
print("Unique C_1m:", uniq_1m)
for i in range(len(uniq_1m)):
    for j in range(i+1, len(uniq_1m)):
        d = uniq_1m[j] - uniq_1m[i]
        print(f"{uniq_1m[j]} - {uniq_1m[i]} = {d} (d/9 = {d/9:.2f}, d/24 = {d/24:.2f})")
