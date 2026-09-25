# -*- coding: utf-8 -*-
"""Pantalla 4: Inicio."""

from flask import Blueprint, render_template
from app.database import get_db

main_bp = Blueprint("main", __name__)


@main_bp.route("/inicio")
def inicio():
    db = get_db()
    datos_generales = db.datos_generales.find_one() or {}
    proximo_partido = db.partidos.find_one({"marcador": None}, sort=[("fecha", 1), ("hora", 1)])
    ultimo_resultado = db.partidos.find_one({"marcador": {"$ne": None}})
    grupo_a = db.grupos.find_one({"grupo": "A"})

    return render_template(
        "home.html",
        datos=datos_generales,
        proximo_partido=proximo_partido,
        ultimo_resultado=ultimo_resultado,
        grupo_a=grupo_a,
    )
