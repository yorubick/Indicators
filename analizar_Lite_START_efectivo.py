"""START exacto dentro de una vela1m; distingue ventana19 vs20 vs16 barras nativas."""
import json,datetime
from analizar_C_fuente_vs_grafico import ROOT,read,fit_lite,fit_four_steps,LANES
from analizar_Lite_END_efectivo import compare_lite,reconstruct
def stamp(s):return int(datetime.datetime.fromisoformat(s).timestamp())
def main():
    end=stamp('2026-10-12T19:04:45+00:00');out={}
    for start in ['190000','190015']:
        a=read(f'Lite_START_{start}_chart15_a.csv');b=read(f'Lite_START_{start}_chart15_b.csv')
        t=stamp('2026-10-12T19:00:'+('00' if start=='190000' else '15')+'+00:00')
        window=[r for x,r in b.items() if t<=x<=end]
        assert len(window)==(20 if start=='190000' else 19)
        out[start]={'native_fits':fit_lite(b),'repeat':compare_lite(a,b,0),'inclusive_source_bars':len(window),'range_high':max(float(r['high']) for r in window),'range_low':min(float(r['low']) for r in window)}
    native=read('Lite_START_190015_chart15_b.csv');coarse=read('Lite_START_190015_chart60_b.csv')
    out['coarse_START15']={'independent_C_fits':fit_four_steps(native,coarse),'repeat':compare_lite(read('Lite_START_190015_chart60_a.csv'),coarse,0),'direct_native_levels':compare_lite(native,coarse,45),'reconstruction':reconstruct(native,coarse,'2026-10-12T19:04:45+00:00',19*15*10/183,60,'2026-10-12T19:00:15+00:00')}
    (ROOT/'Lite_START_efectivo.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
    print(json.dumps(out,indent=2))
if __name__=='__main__':main()
