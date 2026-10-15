ratios = [
    0.236, 0.382, 0.500, 0.618, 0.707, 0.750, 0.786, 8/9, 0.886,
    1.000, 1.128, 1.191, 1.200, 1.236, 1.272, 4/3, 1.382, 1.414, 1.500, 1.618
]

print("=== 89 x Ratio ===")
for r in ratios:
    val = 89 * r
    print(f"89 x {r:.4f} = {val:.2f} (round={round(val)})")

print("\n=== 72 x Ratio ===")
for r in ratios:
    val = 72 * r
    print(f"72 x {r:.4f} = {val:.2f} (round={round(val)})")
