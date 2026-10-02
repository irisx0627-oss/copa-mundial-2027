# -*- coding: utf-8 -*-
"""
Quiniela: la gente predice el marcador de los partidos y gana puntos e
insignias. NO hay dinero de por medio en ningun momento.
"""

from functools import wraps
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from bson.objectid import ObjectId
from bson.errors import InvalidId

from app.database import get_db
from app.quiniela_logic import calcular_puntos, calcular_insignias
from database.seed_data import INSIGNIAS

quiniela_bp = Blueprint("quiniela", __name__)


def login_requerido(vista):
    """Decorador sencillo: si no hay sesion iniciada, manda a login."""
    @wraps(vista)
    def envoltura(*args, **kwargs):
        if not session.get("usuario_id"):
            flash("Inicia sesion para usar la quiniela.")
            return redirect(url_for("auth.login"))
        return vista(*args, **kwargs)
    return envoltura


@quiniela_bp.route("/partidos/<partido_id>/predecir", methods=["POST"])
@login_requerido
def predecir(partido_id):
    db = get_db()
    try:
        goles_local = int(request.form.get("goles_local", ""))
        goles_visitante = int(request.form.get("goles_visitante", ""))
    except ValueError:
        flash("Escribe un marcador valido (numeros).")
        return redirect(url_for("content.partidos"))

    if goles_local < 0 or goles_visitante < 0:
        flash("El marcador no puede ser negativo.")
        return redirect(url_for("content.partidos"))

    db.predicciones.update_one(
        {"usuario_id": session["usuario_id"], "partido_id": partido_id},
        {"$set": {
            "usuario_id": session["usuario_id"],
            "partido_id": partido_id,
            "goles_local": goles_local,
            "goles_visitante": goles_visitante,
        }},
        upsert=True,
    )
    flash("¡Tu pronostico quedo guardado!")
    return redirect(url_for("content.partidos"))


@quiniela_bp.route("/quiniela")
@login_requerido
def mi_quiniela():
    resumen = obtener_resumen_quiniela(session["usuario_id"])
    return render_template("quiniela.html", **resumen)


def obtener_resumen_quiniela(usuario_id):
    """
    Junta toda la info de la quiniela de un usuario: puntos, insignias y el
    detalle de cada pronostico. La usan tanto /quiniela como Zona +18.
    """
    db = get_db()
    predicciones = list(db.predicciones.find({"usuario_id": usuario_id}))
    filas = []
    puntos_totales = 0

    for pred in predicciones:
        try:
            partido = db.partidos.find_one({"_id": ObjectId(pred["partido_id"])})
        except InvalidId:
            partido = None
        if not partido:
            continue

        estado_manual = pred.get("estado_manual")
        puntos, exacto = calcular_puntos(
            pred["goles_local"], pred["goles_visitante"], partido.get("marcador"), estado_manual
        )
        if puntos:
            puntos_totales += puntos

        filas.append({
            "partido": partido,
            "prediccion": f'{pred["goles_local"]}-{pred["goles_visitante"]}',
            "puntos": puntos,
            "exacto": exacto,
            "jugado": partido.get("marcador") is not None or estado_manual is not None,
        })

    insignias_ganadas = calcular_insignias(puntos_totales, len(predicciones))
    insignias_faltantes = [i for i in INSIGNIAS if i not in insignias_ganadas]

    return {
        "filas": filas,
        "puntos_totales": puntos_totales,
        "total_predicciones": len(predicciones),
        "insignias_ganadas": insignias_ganadas,
        "insignias_faltantes": insignias_faltantes,
    }
