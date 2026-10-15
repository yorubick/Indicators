import json
from pathlib import Path

# Pre-declared predictions for upcoming START sweeps
# 1. Sweep 15:50 (Alcista, End 15:50:00, Baseline 15:30 -> C=69)
# 2. Sweep 07:20 (Lateral, End 07:20:00, Baseline 07:00 -> C=75)

predictions = {
    'sweep_1550_alcista': {
        'description': 'END fijo 15:50:00, barrido de START hacia adelante (n < 21) y atras (n >= 21)',
        'baseline': {'START': '15:30:00', 'END': '15:50:00', 'bars': 21, 'C_measured': 69.0},
        'predictions': [
            {'START': '15:31:00', 'bars': 20, 'predicted_C': 65.57377049, 'regime': 'short_branch_exact'},
            {'START': '15:32:00', 'bars': 19, 'predicted_C': 62.29508197, 'regime': 'short_branch_exact'},
            {'START': '15:33:00', 'bars': 18, 'predicted_C': 60.00000000, 'regime': 'short_branch_exact_floor'},
            {'START': '15:29:00', 'bars': 22, 'predicted_C_candidates': [69.0, 71.0, 72.0], 'notes': 'Range frozen at 87.75 pts'},
            {'START': '15:28:00', 'bars': 23, 'predicted_C_candidates': [69.0, 71.0, 75.0], 'notes': 'Range frozen at 87.75 pts'}
        ]
    },
    'sweep_0720_lateral': {
        'description': 'END fijo 07:20:00, barrido de START hacia adelante (n < 21) y atras (n >= 21)',
        'baseline': {'START': '07:00:00', 'END': '07:20:00', 'bars': 21, 'C_measured': 75.0},
        'predictions': [
            {'START': '07:01:00', 'bars': 20, 'predicted_C': 65.57377049, 'regime': 'short_branch_exact'},
            {'START': '07:02:00', 'bars': 19, 'predicted_C': 62.29508197, 'regime': 'short_branch_exact'},
            {'START': '07:03:00', 'bars': 18, 'predicted_C': 60.00000000, 'regime': 'short_branch_exact_floor'},
            {'START': '06:59:00', 'bars': 22, 'predicted_C_candidates': [75.0, 77.0], 'notes': 'Range frozen at 37.50 pts'},
            {'START': '06:58:00', 'bars': 23, 'predicted_C_candidates': [75.0, 77.0], 'notes': 'Range frozen at 37.50 pts'}
        ]
    }
}

out_p = Path(r"C:\Users\PC\.gemini\antigravity\brain\0d7f3bfd-8524-49c4-8cc4-be41c8fbcb27\scratch\predicciones_barrido_start.json")
out_p.write_text(json.dumps(predictions, indent=2))
print("Saved predictions to scratch/predicciones_barrido_start.json")
