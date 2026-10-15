import json
import pandas as pd

def main():
    data = json.load(open('data/barrido_start_1933.json', 'r', encoding='utf-8'))
    df = pd.read_csv('data/exports/20261012_start_191400_end_193300_15s.csv')
    df['dt'] = pd.to_datetime(df['time'], unit='s', utc=True)

    end_time = '2026-10-12 19:33:00+00:00'

    print('| START | C_off | C_base | Delta | Range_H | Range_L | Height | Start_O | Start_H | Start_L | Start_C | Vol |')
    print('|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|')

    for c in data['cases']:
        start_str = c['START'].replace('Z', '+00:00')
        c_off = round(c['C_resuelto'])
        t = c['T_seg']
        dt_src = c['source_interval_seconds']
        n_inc = (t // dt_src) + 1
        c_base = round((n_inc * dt_src * 10) / 183)
        delta = c_off - c_base

        mask = (df['dt'] >= start_str) & (df['dt'] <= end_time)
        sub = df[mask]

        rH = sub['high'].max()
        rL = sub['low'].min()
        rHeight = rH - rL

        first_bar = sub.iloc[0]

        print(f"| {start_str[11:16]} | {c_off:5d} | {c_base:6d} | {delta:+5d} | {rH:9.2f} | {rL:9.2f} | {rHeight:6.2f} | {first_bar['open']:9.2f} | {first_bar['high']:9.2f} | {first_bar['low']:9.2f} | {first_bar['close']:9.2f} | {int(first_bar['Volume']):5d} |")

if __name__ == '__main__':
    main()
