actual_15s = {
    "19:23": 88, "19:24": 67, "19:25": 88, "19:26": 88, "19:27": 79,
    "19:28": 102, "19:29": 123, "19:30": 67, "19:31": 87, "19:32": 106,
    "19:33": 87, "19:34": 123, "19:35": 87
}

print("=== 15S RESIDUALS AGAINST BASE T/18.3 ===")
for dt in sorted(actual_15s.keys()):
    m_diff = int(dt.split(":")[1]) - 3
    T = m_diff * 60
    base = round(T / 18.3)
    c_obs = actual_15s[dt]
    diff = c_obs - base
    print(f"{dt} | T={T:4d}s | Base={base:3d} | C_15s={c_obs:3d} | Diff={diff:+3d} | C/Base={c_obs/base:.2f}")
