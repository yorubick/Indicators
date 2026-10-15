import master_cases

print("=== TESTING RETRACEMENT RATIO AS SELECTOR ===")
# Let's test if Retracement Ratio = (H_last - C_end) / (H_last - L_last)
# maps monotonically to C!

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
        
        c_end = sub[-1]['close']
        h_last = last_sh[1]
        l_last = last_sl[1]
        amp = abs(h_last - l_last)
        
        # Retracement from high:
        ret = (h_last - c_end) / amp if amp > 0 else 0
        
        print(f"END {d['e']} | C={d['C']:3d} | H_last={h_last:.2f} | L_last={l_last:.2f} | C_end={c_end:.2f} | Amp={amp:5.2f} | Retracement={ret:6.3f}")
