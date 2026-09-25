# -*- coding: utf-8 -*-
"""
Pantallas 5 a 13 y 15: Partidos, Selecciones, Grupos, Eliminatorias, Jugadores,
Estadios, Ciudades sede, Mexico, Historia del Mundial, Noticias.
"""

from flask import Blueprint, render_template, request, session
from app.database import get_db

content_bp = Blueprint("content", __name__)


# ---------- 5. PARTIDOS ----------
@content_bp.route("/partidos")
def partidos():
    db = get_db()
    filtro = request.args.get("filtro", "todos")  # todos | hoy | manana | fase_grupos
    partidos = list(db.partidos.find().sort([("fecha", 1), ("hora", 1)]))

    # Si el usuario tiene sesion iniciada, le mostramos sus predicciones ya hechas
    predicciones_usuario = {}
    if session.get("usuario_id"):
        preds = db.predicciones.find({"usuario_id": session["usuario_id"]})
        predicciones_usuario = {p["partido_id"]: p for p in preds}

    for p in partidos:
        p["_id_str"] = str(p["_id"])
        p["mi_prediccion"] = predicciones_usuario.get(p["_id_str"])

    return render_template("partidos.html", partidos=partidos, filtro=filtro)


# ---------- 6. SELECCIONES ----------
@content_bp.route("/selecciones")
def selecciones():
    db = get_db()
    busqueda = request.args.get("q", "").strip()
    confederacion = request.args.get("confederacion", "todos")

    consulta = {}
    if busqueda:
        consulta["nombre"] = {"$regex": busqueda, "$options": "i"}
    if confederacion != "todos":
        consulta["confederacion"] = confederacion

    selecciones = list(db.selecciones.find(consulta).sort("nombre", 1))
    confederaciones = sorted(db.selecciones.distinct("confederacion"))
    return render_template(
        "selecciones.html", selecciones=selecciones, confederaciones=confederaciones,
        busqueda=busqueda, confederacion_activa=confederacion,
    )


# ---------- 7. GRUPOS ----------
@content_bp.route("/grupos")
def grupos():
    db = get_db()
    grupos = list(db.grupos.find().sort("grupo", 1))
    return render_template("grupos.html", grupos=grupos)


@content_bp.route("/grupos/<letra>")
def detalle_grupo(letra):
    db = get_db()
    grupo = db.grupos.find_one({"grupo": letra.upper()})
    return render_template("grupos.html", grupos=[grupo] if grupo else [], grupo_detalle=grupo)


# ---------- 8. ELIMINATORIAS ----------
@content_bp.route("/eliminatorias")
def eliminatorias():
    # Las llaves de eliminacion directa se arman cuando termina la fase de grupos.
    # Por ahora mostramos la estructura vacia: Dieciseisavos, Octavos, Cuartos, Semifinal, Final.
    fases = ["Dieciseisavos", "Octavos", "Cuartos", "Semifinal", "Final"]
    return render_template("eliminatorias.html", fases=fases)


# ---------- 9. JUGADORES ----------
@content_bp.route("/jugadores")
def jugadores():
    db = get_db()
    vista = request.args.get("vista", "destacados")  # destacados | por_seleccion | por_posicion

    if vista == "destacados":
        jugadores = list(db.jugadores.find({"destacado": True}).sort("nombre", 1))
    elif vista == "por_posicion":
        jugadores = list(db.jugadores.find().sort([("posicion", 1), ("nombre", 1)]))
    else:  # por_seleccion (y por defecto)
        jugadores = list(db.jugadores.find().sort([("seleccion", 1), ("nombre", 1)]))

    banderas = {s["nombre"]: s["bandera"] for s in db.selecciones.find()}
    banderas_url = {s["nombre"]: s.get("bandera_url") for s in db.selecciones.find()}
    for j in jugadores:
        j["bandera"] = banderas.get(j["seleccion"], "🏳️")
        j["bandera_url"] = banderas_url.get(j["seleccion"])

    return render_template("jugadores.html", jugadores=jugadores, vista=vista, total=db.jugadores.count_documents({}))


# ---------- 10. ESTADIOS ----------
@content_bp.route("/estadios")
def estadios():
    db = get_db()
    pais_filtro = request.args.get("pais", "todos")
    consulta = {} if pais_filtro == "todos" else {"pais": pais_filtro}
    estadios = list(db.estadios.find(consulta).sort("ciudad", 1))
    paises = sorted(db.estadios.distinct("pais"))
    return render_template("estadios.html", estadios=estadios, paises=paises, pais_activo=pais_filtro)


# ---------- 11. CIUDADES SEDE ----------
@content_bp.route("/ciudades-sede")
def ciudades_sede():
    db = get_db()
    ciudades = list(db.ciudades_sede.find().sort("num", 1))
    por_pais = {}
    for c in ciudades:
        por_pais.setdefault(c["pais"], []).append(c)
    return render_template("ciudades.html", por_pais=por_pais)


# ---------- 12. MEXICO ----------
@content_bp.route("/mexico")
def mexico():
    db = get_db()
    estadios_mx = list(db.estadios.find({"pais": "Mexico"}))
    partidos_mx = list(db.partidos.find({"$or": [{"local": "Mexico"}, {"visitante": "Mexico"}]}))
    jugadores_mx = list(db.jugadores.find({"seleccion": "Mexico"}))
    grupo_mx = db.grupos.find_one({"equipos": "Mexico"})
    return render_template(
        "mexico.html", estadios=estadios_mx, partidos=partidos_mx,
        jugadores=jugadores_mx, grupo=grupo_mx,
    )


# ---------- 13. HISTORIA DEL MUNDIAL ----------
@content_bp.route("/historia")
def historia():
    db = get_db()
    campeones = list(db.historia_mundial.find().sort("anio", -1))
    return render_template("historia.html", campeones=campeones)


# ---------- 15. NOTICIAS ----------
@content_bp.route("/noticias")
def noticias():
    db = get_db()
    categoria = request.args.get("categoria", "Todas")
    consulta = {} if categoria == "Todas" else {"categoria": categoria}
    noticias = list(db.noticias.find(consulta).sort("horas", 1))
    categorias = ["Todas"] + sorted(db.noticias.distinct("categoria"))
    return render_template("noticias.html", noticias=noticias, categorias=categorias, categoria_activa=categoria)
