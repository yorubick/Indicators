import master_cases

print("=== TESTING LAST SWINGS BEFORE END IN END SWEEP ===")
# START is 18:55:00
for d in master_cases.dataset:
    if d['s'] == '18:55:00' and d['dt'] == 15 and '19:18' <= d['e'] <= '19:22':
        sub = d['sub']
        n = len(sub)
        # Find all swing highs and lows
        shs = []
        sls = []
        for i in range(1, n-1):
            if sub[i]['high'] >= sub[i-1]['high'] and sub[i]['high'] >= sub[i+1]['high']:
                shs.append((i, sub[i]['high']))
            if sub[i]['low'] <= sub[i-1]['low'] and sub[i]['low'] <= sub[i+1]['low']:
                sls.append((i, sub[i]['low']))
                
        last_sh = shs[-1] if shs else (0, 0)
        last_sl = sls[-1] if sls else (0, 0)
        
        bars_since_sh = n - 1 - last_sh[0]
        bars_since_sl = n - 1 - last_sl[0]
        
        # Last swing amplitude:
        last_swing_amp = abs(last_sh[1] - last_sl[1])
        
        print(f"END {d['e']} | C={d['C']:3d} | Last SH: bar {last_sh[0]:3d} ({last_sh[1]:.2f}, t-{bars_since_sh*15:2d}s) | Last SL: bar {last_sl[0]:3d} ({last_sl[1]:.2f}, t-{bars_since_sl*15:2d}s) | Amp={last_swing_amp:.2f}")
