import re

# Comprehensive list of Pine Script v5 / v6 built-ins
builtins = {
    'indicator', 'overlay', 'input', 'time', 'timestamp', 'group', 'minval', 'options',
    'high', 'low', 'open', 'close', 'timeframe', 'math', 'max', 'min', 'floor', 'round',
    'nz', 'na', 'plot', 'color', 'new', 'style_linebr', 'str', 'tostring', 'table',
    'position', 'top_right', 'barstate', 'islast', 'isseconds', 'isminutes', 'multiplier',
    'red', 'green', 'blue', 'navy', 'teal', 'orange', 'maroon', 'yellow', 'olive', 'lime',
    'aqua', 'purple', 'fuchsia', 'black', 'gray', 'white'
}

with open(r'C:\Users\PC\.gemini\antigravity\brain\0d7f3bfd-8524-49c4-8cc4-be41c8fbcb27\scratch\PoiSzn_C_Deterministic_Lab_v4.pine', encoding='utf-8') as f:
    text = f.read()

# Add 'ep' declaration to text
text_fixed = text.replace(
    'float sp = rng_pts > 0 ? (start_open - rng_low) / rng_pts : 0.5\n            bool is_bull = close > start_open',
    'float sp = rng_pts > 0 ? (start_open - rng_low) / rng_pts : 0.5\n            float ep = rng_pts > 0 ? (close - rng_low) / rng_pts : 0.5\n            bool is_bull = close > start_open'
)

# Also check version 6
text_fixed = text_fixed.replace('//@version=5', '//@version=6')

with open(r'C:\Users\PC\.gemini\antigravity\brain\0d7f3bfd-8524-49c4-8cc4-be41c8fbcb27\scratch\PoiSzn_C_Deterministic_Lab_v4.pine', 'w', encoding='utf-8') as f:
    f.write(text_fixed)

print("Pine script v4.0 updated with 'ep' and '@version=6' successfully!")
