import json
from pathlib import Path

p = Path("G:/trading/guias/analisis/C_dataset_verificado.json")
with open(p, "r", encoding="utf-8") as f:
    d = json.load(f)

# Look at 19:01:
# When n=21 (19:01 to 19:21): C = 77
# When n=22 (19:01 to 19:22): C = 77
# When n=23 (19:01 to 19:23): C = 77
# When n=24 (19:01 to 19:24): C = 77

# What was C calculated from at 19:21?
# At 19:21, n was 21 bars!
# In the short branch formula, what does n=21 give?
# n * 200 / 61 = 21 * 200 / 61 = 68.85
# But here C is 77!
# 77 - 68.85 = +8.15 seconds.

# What about 06:00 to 06:20 (n=21): C = 77!
# 06:00 to 06:21 (n=22): C = 77!
# 06:00 to 06:22 (n=23): C = 77!
# Again, C is 77!

# Why is C = 77 appearing so often?
# Let's count how many times each C appears across all 59 long cases!
long_cases = [c for c in d["cases"] if c["branch"] == "long"]
from collections import Counter
c_counts = Counter([round(c["C"]) for c in long_cases if c["dt"] == 60])
print("Frequencies of C values across ALL 60s long cases:")
for val, count in c_counts.most_common():
    print(f"  C = {val:3d}: {count:2d} times")
