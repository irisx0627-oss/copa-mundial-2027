# -*- coding: utf-8 -*-
"""
Logica de la Quiniela: calcular puntos de una prediccion contra el resultado
real, y calcular que insignias le tocan a un usuario segun su historial.

Nada de esto mueve dinero: son puntos e insignias dentro de la app.
"""

from database.seed_data import PUNTOS_MARCADOR_EXACTO, PUNTOS_RESULTADO_CORRECTO, INSIGNIAS


def _resultado(goles_local, goles_visitante):
    """Devuelve 'L' si gana el local, 'V' si gana el visitante, 'E' si empatan."""
    if goles_local > goles_visitante:
        return "L"
    if goles_local < goles_visitante:
        return "V"
    return "E"


def calcular_puntos(prediccion_local, prediccion_visitante, marcador_real, estado_manual=None):
    """
    marcador_real: string tipo "2-1" (como se guarda en la coleccion 'partidos').
    estado_manual: si el administrador decidio el resultado de este pronostico a mano
        (porque el partido aun no tiene marcador real, por ejemplo), puede ser:
        "exacto" (acerto el marcador exacto), "resultado" (acerto quien gana/empate,
        pero no el marcador), "no" (no acerto), o None (usar el calculo automatico).
    Devuelve (puntos, es_exacto) o (None, None) si no hay forma de saber el resultado.
    """
    if estado_manual == "exacto":
        return PUNTOS_MARCADOR_EXACTO, True
    if estado_manual == "resultado":
        return PUNTOS_RESULTADO_CORRECTO, False
    if estado_manual == "no":
        return 0, False

    if not marcador_real:
        return None, None

    try:
        real_local, real_visitante = [int(x) for x in marcador_real.split("-")]
    except (ValueError, AttributeError):
        return None, None

    if prediccion_local == real_local and prediccion_visitante == real_visitante:
        return PUNTOS_MARCADOR_EXACTO, True

    if _resultado(prediccion_local, prediccion_visitante) == _resultado(real_local, real_visitante):
        return PUNTOS_RESULTADO_CORRECTO, False

    return 0, False


def calcular_insignias(puntos_totales, total_predicciones):
    """Devuelve la lista de insignias (dict) que el usuario ya se gano."""
    ganadas = []
    for insignia in INSIGNIAS:
        cumple_puntos = puntos_totales >= insignia["requisito_puntos"]
        cumple_predicciones = total_predicciones >= insignia["requisito_predicciones"]
        if cumple_puntos and cumple_predicciones:
            ganadas.append(insignia)
    return ganadas
