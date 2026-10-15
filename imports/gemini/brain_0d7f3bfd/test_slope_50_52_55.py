import fractions

# We have:
# n=21 -> 50
# n=22 -> 52
# n=23 -> 55

for num in range(1, 200):
    for den in range(1, 100):
        c21 = round(21 * num / den)
        c22 = round(22 * num / den)
        c23 = round(23 * num / den)
        if c21 == 50 and c22 == 52 and c23 == 55:
            frac = fractions.Fraction(num, den)
            print(f"Match: {num}/{den} = {num/den:.6f} -> n=21:{c21}, n=22:{c22}, n=23:{c23}")
            break
