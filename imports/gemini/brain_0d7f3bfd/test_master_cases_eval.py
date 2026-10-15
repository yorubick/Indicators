import master_cases

# Test the master cases
print("=== TESTING MODEL ON REMAINING MASTER CASES ===")
for d in master_cases.dataset:
    s = d['s']
    e = d['e']
    B = d['bars']
    dt = d['dt']
    C = d['C']
    if dt == 60:
        # Check if B < 21
        if B < 21:
            pred = max(float(dt), B * dt * 10.0 / 183.0)
            err = abs(C - pred)
            print(f"Morning/Short 1m [{s} -> {e}] B={B:2d} Act={C:6.2f} Pred={pred:6.2f} Err={err:6.4f}")
        else:
            print(f"Master 1m [{s} -> {e}] B={B:2d} Act={C:6.2f} Range={d['range']:.2f}")
    elif dt == 15:
        if B < 21:
            pred = max(float(dt), B * dt * 10.0 / 183.0)
            err = abs(C - pred)
            print(f"Short 15s [{s} -> {e}] B={B:2d} Act={C:6.2f} Pred={pred:6.2f} Err={err:6.4f}")
