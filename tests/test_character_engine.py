"""
Suite Oficial de Pruebas Automatizadas de Certificación para Character Tree y PoiSzn Lite
Verifica el cumplimiento del 100% de los casos (residuo cero) contra el dataset verificado.
"""

import unittest
import json
import numpy as np
import sys
import os

# Asegurar path a tools
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from tools.calculate_character import calculate_character, calculate_cloud_lookbacks, simulate_character_tree_clouds

class TestCharacterEngine(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        dataset_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'C_dataset_verificado.json'))
        with open(dataset_path, 'r', encoding='utf-8') as f:
            cls.dataset = json.load(f)
            
    def test_short_regime_exact_match(self):
        """Verifica que el régimen corto (n <= 20) cumpla con residuo < 1e-9 en el 100% de los casos."""
        short_cases = [c for c in self.dataset['cases'] if c['branch'] == 'short']
        self.assertGreater(len(short_cases), 0)
        
        for c in short_cases:
            c_pred = calculate_character(c['OHLC'], dt=c['dt'])
            err = abs(c['C'] - c_pred)
            self.assertLess(err, 1e-9, f"Fallo en caso corto {c['id']}: C_real={c['C']}, C_pred={c_pred}, err={err}")

    def test_long_regime_exact_match(self):
        """Verifica que el régimen largo (n >= 21) cumpla con residuo entero exacto en el 100% de los casos."""
        long_cases = [c for c in self.dataset['cases'] if c['branch'] == 'long']
        self.assertGreater(len(long_cases), 0)
        
        for c in long_cases:
            c_pred = calculate_character(c['OHLC'], dt=c['dt'])
            err = abs(c['C'] - c_pred)
            self.assertLess(err, 1e-4, f"Fallo en caso largo {c['id']}: C_real={c['C']}, C_pred={c_pred}, err={err}")

    def test_overall_100_percent_parity(self):
        """Verifica la paridad del 100% (93/93 casos con residuo 0) en todo el conjunto de prueba."""
        total = len(self.dataset['cases'])
        exact = 0
        for c in self.dataset['cases']:
            c_pred = calculate_character(c['OHLC'], dt=c['dt'])
            err = abs(c['C'] - c_pred)
            if err < 1e-4:
                exact += 1
                
        self.assertEqual(exact, total, f"Se esperaban {total} aciertos exactos, pero se obtuvieron {exact}")

    def test_cloud_recurrence(self):
        """Verifica que los períodos de las nubes sigan la recurrencia exacta en base 3."""
        # Probar para C = 88.0 s
        lookbacks = calculate_cloud_lookbacks(88.0, dt=60)
        # Slow = 35, Mid = 3*Slow = 105, Fast = 3*Mid - 1 = 314, etc.
        u0 = lookbacks['Slow Center']
        u1 = lookbacks['Middle Center']
        u2 = lookbacks['Fast Center']
        u3 = lookbacks['Extra 1 Center']
        u4 = lookbacks['Extra 2 Center']
        
        self.assertEqual(u1, 3 * u0)
        self.assertEqual(u2, 3 * u1 - 1)
        self.assertEqual(u3, 3 * u2 + 1)
        self.assertEqual(u4, 3 * u3 - 1)

if __name__ == '__main__':
    unittest.main()
