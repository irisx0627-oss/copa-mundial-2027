# -*- coding: utf-8 -*-
"""Pantallas 14, 16 y 17: Quiz, Ajustes, Zona +18."""

from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from app.database import get_db
from app.routes.quiniela import login_requerido

extras_bp = Blueprint("extras", __name__)


# ---------- 14. QUIZ ----------
@extras_bp.route("/quiz")
def quiz():
    db = get_db()
    preguntas = list(db.quiz_preguntas.find())
    return render_template("quiz.html", preguntas=preguntas, resultado=None)


@extras_bp.route("/quiz/calificar", methods=["POST"])
def calificar_quiz():
    db = get_db()
    preguntas = list(db.quiz_preguntas.find())
    aciertos = 0
    for i, p in enumerate(preguntas):
        respuesta_usuario = request.form.get(f"pregunta_{i}")
        if respuesta_usuario == p["respuesta"]:
            aciertos += 1
    return render_template("quiz.html", preguntas=preguntas, resultado=aciertos, total=len(preguntas))


# ---------- 16. AJUSTES ----------
@extras_bp.route("/ajustes")
def ajustes():
    usuario = None
    if session.get("usuario_id"):
        from bson.objectid import ObjectId
        db = get_db()
        usuario = db.usuarios.find_one({"_id": ObjectId(session["usuario_id"])})
    tema_actual = session.get("tema", "oscuro")
    return render_template("ajustes.html", usuario=usuario, tema_actual=tema_actual)


# ---------- Perfil ----------
@extras_bp.route("/ajustes/perfil", methods=["GET", "POST"])
@login_requerido
def perfil():
    from bson.objectid import ObjectId
    db = get_db()
    usuario_id = ObjectId(session["usuario_id"])
    usuario = db.usuarios.find_one({"_id": usuario_id})

    if request.method == "POST":
        accion = request.form.get("accion")

        if accion == "datos":
            nombre = request.form.get("nombre", "").strip()
            fecha_nacimiento = request.form.get("fecha_nacimiento", "").strip()
            if not nombre:
                flash("El nombre no puede quedar vacio.")
            else:
                db.usuarios.update_one(
                    {"_id": usuario_id},
                    {"$set": {"nombre": nombre, "fecha_nacimiento": fecha_nacimiento}},
                )
                session["nombre"] = nombre
                flash("Tus datos se actualizaron.")

        elif accion == "contrasena":
            actual = request.form.get("contrasena_actual", "")
            nueva = request.form.get("nueva_contrasena", "")
            confirmar = request.form.get("confirmar_contrasena", "")

            if not check_password_hash(usuario["contrasena_hash"], actual):
                flash("Tu contraseña actual no es correcta.")
            elif nueva != confirmar:
                flash("Las contraseñas nuevas no coinciden.")
            elif len(nueva) < 4:
                flash("La contraseña nueva es muy corta.")
            else:
                db.usuarios.update_one(
                    {"_id": usuario_id},
                    {"$set": {"contrasena_hash": generate_password_hash(nueva)}},
                )
                flash("Tu contraseña se actualizo correctamente.")

        return redirect(url_for("extras.perfil"))

    return render_template("perfil.html", usuario=usuario)


# ---------- Notificaciones ----------
@extras_bp.route("/ajustes/notificaciones/toggle", methods=["POST"])
@login_requerido
def notificaciones_toggle():
    from bson.objectid import ObjectId
    db = get_db()
    usuario_id = ObjectId(session["usuario_id"])
    usuario = db.usuarios.find_one({"_id": usuario_id})
    nuevo_valor = not usuario.get("notificaciones_activadas", True)
    db.usuarios.update_one({"_id": usuario_id}, {"$set": {"notificaciones_activadas": nuevo_valor}})
    return redirect(url_for("extras.ajustes"))


# ---------- Idioma ----------
@extras_bp.route("/ajustes/idioma", methods=["GET", "POST"])
def idioma():
    if request.method == "POST":
        idioma_elegido = request.form.get("idioma", "es")
        if idioma_elegido != "es":
            flash("Por ahora la app solo esta disponible en Español. ¡Pronto mas idiomas!")
            return redirect(url_for("extras.idioma"))
        session["idioma"] = "es"
        if session.get("usuario_id"):
            from bson.objectid import ObjectId
            db = get_db()
            db.usuarios.update_one({"_id": ObjectId(session["usuario_id"])}, {"$set": {"idioma": "es"}})
        flash("Idioma actualizado.")
        return redirect(url_for("extras.ajustes"))

    return render_template("idioma.html", idioma_actual=session.get("idioma", "es"))


# ---------- Tema ----------
@extras_bp.route("/ajustes/tema", methods=["GET", "POST"])
def tema():
    if request.method == "POST":
        tema_elegido = request.form.get("tema", "oscuro")
        if tema_elegido not in ("oscuro", "claro"):
            tema_elegido = "oscuro"
        session["tema"] = tema_elegido
        if session.get("usuario_id"):
            from bson.objectid import ObjectId
            db = get_db()
            db.usuarios.update_one({"_id": ObjectId(session["usuario_id"])}, {"$set": {"tema": tema_elegido}})
        flash("Tema actualizado.")
        return redirect(url_for("extras.ajustes"))

    return render_template("tema.html", tema_actual=session.get("tema", "oscuro"))


# ---------- Privacidad ----------
@extras_bp.route("/ajustes/privacidad")
def privacidad():
    return render_template("privacidad.html")


# ---------- Ayuda ----------
@extras_bp.route("/ajustes/ayuda")
def ayuda():
    return render_template("ayuda.html")


# ---------- 17. ZONA +18 ----------
# Unicamente informativa/restringida. Dentro solo mostramos la quiniela de
# puntos e insignias (sin dinero real), NUNCA apuestas con dinero.
@extras_bp.route("/zona-18", methods=["GET", "POST"])
def zona_18():
    verificado = session.get("edad_verificada", False)

    if request.method == "POST":
        fecha_nacimiento = request.form.get("fecha_nacimiento", "")
        try:
            nacimiento = datetime.strptime(fecha_nacimiento, "%Y-%m-%d")
            edad = (datetime.utcnow() - nacimiento).days // 365
            if edad >= 18:
                session["edad_verificada"] = True
                verificado = True
        except ValueError:
            verificado = False

    resumen = {}
    if verificado and session.get("usuario_id"):
        from app.routes.quiniela import obtener_resumen_quiniela
        resumen = obtener_resumen_quiniela(session["usuario_id"])

    return render_template("zona18.html", verificado=verificado, **resumen)
