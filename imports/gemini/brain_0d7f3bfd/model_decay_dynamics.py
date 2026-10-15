import master_cases
import numpy as np

print("Testing dynamic decay models on END sweep and Morning series...")

# Let's focus on the two pure decay sequences where Range is constant:
# Sequence A: 1m Morning (Range = 32.50)
# 05:15 (31 bars) -> 116
# 05:25 (41 bars) -> 113
# 05:30 (46 bars) -> 110

# Sequence B: 15s 19:21 (Range = 24.50, dt = 15s)
# 19:21:00 (105 bars) -> 115
# 19:21:15 (106 bars) -> 106
# 19:21:30 (107 bars) -> 79
# 19:21:45 (108 bars) -> 66

# Sequence C: 15s 19:20 (Range = 22.75, dt = 15s)
# 19:20:00 (101 bars) -> 106
# 19:20:15 (102 bars) -> 79
# 19:20:30 (103 bars) -> 67
# 19:20:45 (104 bars, new high 24.50) -> 66

# Notice that in Sequence B, 1 bar (15 seconds) drops C by 9 points (115 -> 106),
# next bar drops C by 27 points (106 -> 79),
# next bar drops C by 13 points (79 -> 66).
# Whereas in Sequence A, 10 bars (10 minutes) only drops C by 3 points (116 -> 113)!
# Why would 10 bars of 1m drop C by 3 points, while 1 bar of 15s drops C by 9 or 27 points?
# Because the price moved inside the bar!
