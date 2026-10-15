"""Reconstrucción causal Manual con C proporcionado, no un generador de C.

Calcula las dos semillas en paralelo desde END. Selecciona/publica una rama
solo al primer cierre posterior estrictamente fuera del rango global.
Alcance: primeras curvas de las exportaciones Manual comprobadas.
"""
from familia_ema import periodos

class FlujoManual:
    def __init__(self,C_seconds,source_seconds,range_high,range_low,end_high,end_low):
        self.periods=periodos(C_seconds,source_seconds)
        self.high=range_high;self.low=range_low;self.side=None
        self.branches={'bull':dict.fromkeys(self.periods,end_low),
                       'bear':dict.fromkeys(self.periods,end_high)}

    def closed_bar_after_END(self,close):
        """Una llamada por vela fuente cerrada, empezando después de END."""
        for state in self.branches.values():
            for k,n in self.periods.items():state[k]+=2/(n+1)*(close-state[k])
        if self.side is None:
            if close>self.high:self.side='bull'
            elif close<self.low:self.side='bear'
        return dict(self.branches[self.side]) if self.side else None
