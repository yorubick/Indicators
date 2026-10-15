import master_cases

print("=== TESTING CSD / INDUCEMENT HYPOTHESIS ===")
# In ICT / PoiSzn:
# An Inducement (IDM) is the first internal swing low (in an uptrend) or swing high (in a downtrend).
# Let's find the first internal swing high/low after START.

for d in master_cases.dataset:
    if d['bars'] >= 21 and d['dt'] == 15 and '18:54' <= d['s'] <= '18:57':
        sub = d['sub']
        n = len(sub)
        # Find first swing high and low after bar 0
        first_sh = None
        first_sl = None
        for i in range(1, min(15, n-1)):
            if sub[i]['high'] > sub[i-1]['high'] and sub[i]['high'] > sub[i+1]['high']:
                if first_sh is None: first_sh = (i, sub[i]['high'])
            if sub[i]['low'] < sub[i-1]['low'] and sub[i]['low'] < sub[i+1]['low']:
                if first_sl is None: first_sl = (i, sub[i]['low'])
                
        sh_str = f"bar {first_sh[0]} ({first_sh[1]:.2f})" if first_sh else "None"
        sl_str = f"bar {first_sl[0]} ({first_sl[1]:.2f})" if first_sl else "None"
        print(f"START {d['s']} | C={d['C']:3d} | 1st SH: {sh_str} | 1st SL: {sl_str} | Start O={sub[0]['open']:.2f} H={sub[0]['high']:.2f} L={sub[0]['low']:.2f} C={sub[0]['close']:.2f}")
