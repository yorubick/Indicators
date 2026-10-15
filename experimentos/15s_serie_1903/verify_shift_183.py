# Check delta T / delta C
T_1903 = 1800 # 30 min (19:03 to 19:33)
T_1908 = 1500 # 25 min (19:08 to 19:33)

C_1903 = 87
C_1908 = 70

delta_T = T_1903 - T_1908 # 300s
delta_C = C_1903 - C_1908 # 17s

ratio = delta_T / delta_C
print(f"delta_T = {delta_T} s")
print(f"delta_C = {delta_C} s")
print(f"delta_T / delta_C = {ratio:.4f}")
print(f"delta_T / 18.3 = {delta_T / 18.3:.4f}")
print(f"87 - round(delta_T / 18.3) = {87 - round(delta_T / 18.3)}")
