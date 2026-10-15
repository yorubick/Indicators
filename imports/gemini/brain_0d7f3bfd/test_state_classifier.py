import master_cases
import numpy as np

# Let's test a machine learning decision tree on the 40 cases of n >= 21
dataset = [d for d in master_cases.dataset if d['bars'] >= 21]

features = []
targets = []

for d in dataset:
    sub = d['sub']
    H = max(b['high'] for b in sub)
    L = min(b['low'] for b in sub)
    Rng = H - L
    
    # Extract features from start, end, and range:
    O0 = sub[0]['open']
    H0 = sub[0]['high']
    L0 = sub[0]['low']
    C0 = sub[0]['close']
    
    C_end = sub[-1]['close']
    H_end = sub[-1]['high']
    L_end = sub[-1]['low']
    
    n = d['bars']
    dt = d['dt']
    
    # Normalized features:
    f = [
        (O0 - L) / Rng,            # Start relative position (0 to 1)
        (C0 - O0) / Rng,           # Start candle body relative to range
        (H0 - L0) / Rng,           # Start candle range relative to range
        (H - C_end) / Rng,         # End retracement from high
        (C_end - L_end) / (H_end - L_end) if H_end > L_end else 0.5, # End bar pin position
        Rng,                       # Absolute range in points
        n,                         # Number of bars
        dt,                        # Resolution in seconds
        (H - sub[0]['high']) / Rng,# Distance of start high to global high
        (sub[0]['low'] - L) / Rng, # Distance of start low to global low
    ]
    features.append(f)
    targets.append(d['C'])

features = np.array(features)
targets = np.array(targets)

print(f"Dataset shape: {features.shape}, Targets: {len(targets)}")

# Let's inspect correlations with targets:
feature_names = [
    "Start_Rel_Pos", "Start_Body_Norm", "Start_Rng_Norm", "End_Ret_Norm",
    "End_Pin_Pos", "Abs_Range", "Bars_n", "Res_dt", "Dist_to_High", "Dist_to_Low"
]

for i, name in enumerate(feature_names):
    corr = np.corrcoef(features[:, i], targets)[0, 1]
    print(f"Feature {name:15s} | Correlation with C: {corr:7.3f}")
