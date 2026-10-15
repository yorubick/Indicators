"""Modelo empirico del perfil B: necesita C, no calcula C desde el rango."""
import math

def periodos(character_seconds, source_seconds):
    if character_seconds <= 0 or source_seconds <= 0:
        raise ValueError('C y la resolucion deben ser positivos')
    result={}
    for label,factor in [('Layer A',1/3),('Layer B',1/9),('Layer C',1/27),
                         ('Extra cloud 1',1),('Extra cloud 2',3)]:
        for suffix,base in [('',72),(' boundary',89)]:
            result[label+suffix]=max(1,math.floor(base*character_seconds*factor/source_seconds+.5))
    return result
