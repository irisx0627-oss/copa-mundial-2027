# -*- coding: utf-8 -*-
"""
Pantallas 1, 2 y 3: Inicio de sesion, Registrarse, Recuperar cuenta.
"""

from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import secrets

from app.database import get_db

auth_bp = Blueprint("auth", __name__)


# ---------- 1. INICIO DE SESION ----------
@auth_bp.route("/", methods=["GET", "POST"])
@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        usuario_o_correo = request.form.get("usuario_o_correo", "").strip()
        contrasena = request.form.get("contrasena", "")

        db = get_db()
        usuario_doc = db.usuarios.find_one({
            "$or": [{"correo": usuario_o_correo}, {"usuario": usuario_o_correo}]
        })

        if usuario_doc and check_password_hash(usuario_doc["contrasena_hash"], contrasena):
            session["usuario_id"] = str(usuario_doc["_id"])
            session["nombre"] = usuario_doc["nombre"]
            session["tema"] = usuario_doc.get("tema", "oscuro")
            session["idioma"] = usuario_doc.get("idioma", "es")
            return redirect(url_for("main.inicio"))

        flash("Usuario/correo o contraseña incorrectos.")
        return redirect(url_for("auth.login"))

    return render_template("login.html")


# ---------- 2. REGISTRARSE ----------
# Flujo pedido: Nombre -> correo -> usuario -> contraseña -> confirmar -> fecha nacimiento -> Crear cuenta
@auth_bp.route("/registrarse", methods=["GET", "POST"])
def registrarse():
    if request.method == "POST":
        nombre = request.form.get("nombre", "").strip()
        correo = request.form.get("correo", "").strip().lower()
        usuario = request.form.get("usuario", "").strip()
        contrasena = request.form.get("contrasena", "")
        confirmar = request.form.get("confirmar_contrasena", "")
        fecha_nacimiento = request.form.get("fecha_nacimiento", "")

        if not all([nombre, correo, usuario, contrasena, confirmar, fecha_nacimiento]):
            flash("Completa todos los campos.")
            return redirect(url_for("auth.registrarse"))

        if contrasena != confirmar:
            flash("Las contraseñas no coinciden.")
            return redirect(url_for("auth.registrarse"))

        db = get_db()
        if db.usuarios.find_one({"$or": [{"correo": correo}, {"usuario": usuario}]}):
            flash("Ya existe una cuenta con ese correo o usuario.")
            return redirect(url_for("auth.registrarse"))

        db.usuarios.insert_one({
            "nombre": nombre,
            "correo": correo,
            "usuario": usuario,
            "contrasena_hash": generate_password_hash(contrasena),
            "fecha_nacimiento": fecha_nacimiento,
            "creado_en": datetime.utcnow(),
            "notificaciones_activadas": True,
            "idioma": "es",
            "tema": "oscuro",
        })

        flash("Cuenta creada. Ahora inicia sesion.")
        return redirect(url_for("auth.login"))

    return render_template("register.html")


# ---------- 3. RECUPERAR CUENTA ----------
# Flujo pedido: correo -> enviar codigo/enlace -> nueva contraseña -> confirmar contraseña
@auth_bp.route("/recuperar", methods=["GET", "POST"])
def recuperar():
    paso = request.args.get("paso", "correo")

    if request.method == "POST":
        if paso == "correo" or request.form.get("accion") == "enviar_codigo":
            correo = request.form.get("correo", "").strip().lower()
            db = get_db()
            usuario_doc = db.usuarios.find_one({"correo": correo})
            if not usuario_doc:
                flash("No encontramos una cuenta con ese correo.")
                return redirect(url_for("auth.recuperar"))

            # Generamos un codigo de 6 digitos y lo guardamos temporalmente.
            # (En produccion aqui se enviaria por correo real con un servicio de email.)
            codigo = f"{secrets.randbelow(1000000):06d}"
            db.usuarios.update_one({"_id": usuario_doc["_id"]}, {"$set": {"codigo_recuperacion": codigo}})
            flash(f"Codigo enviado a {correo}. (Demo: tu codigo es {codigo})")
            return redirect(url_for("auth.recuperar", paso="nueva_contrasena", correo=correo))

        elif request.form.get("accion") == "nueva_contrasena":
            correo = request.form.get("correo", "").strip().lower()
            nueva = request.form.get("nueva_contrasena", "")
            confirmar = request.form.get("confirmar_contrasena", "")

            if nueva != confirmar:
                flash("Las contraseñas no coinciden.")
                return redirect(url_for("auth.recuperar", paso="nueva_contrasena", correo=correo))

            db = get_db()
            db.usuarios.update_one(
                {"correo": correo},
                {"$set": {"contrasena_hash": generate_password_hash(nueva)}, "$unset": {"codigo_recuperacion": ""}},
            )
            flash("Contraseña actualizada. Ya puedes iniciar sesion.")
            return redirect(url_for("auth.login"))

    correo_prellenado = request.args.get("correo", "")
    return render_template("recover.html", paso=paso, correo=correo_prellenado)


# ---------- CERRAR SESION ----------
@auth_bp.route("/cerrar-sesion")
def cerrar_sesion():
    session.clear()
    return redirect(url_for("auth.login"))
