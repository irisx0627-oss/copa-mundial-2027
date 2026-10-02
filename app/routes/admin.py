# -*- coding: utf-8 -*-
"""
Panel de administrador.

Permite a un usuario con es_admin = True agregar, modificar, eliminar y
consultar los datos de cada una de las colecciones del torneo (selecciones,
jugadores, partidos, estadios, ciudades sede, historia, noticias, quiz,
anfitriones y grupos), ademas de otorgar o quitar el rol de administrador a
otros usuarios.

Administrador fijo:
    Cada vez que se corre database/create_collections.py se garantiza que
    exista una cuenta de administrador (ver ADMIN_USUARIO/ADMIN_CORREO/
    ADMIN_CONTRASENA en ese archivo, o en tu .env). Esa cuenta fija no se
    puede degradar desde aqui (ver _ES_ADMIN_FIJO mas abajo), para que
    siempre quede alguien con acceso al panel.
"""

import os
import uuid
from functools import wraps

from bson.objectid import ObjectId
from bson.errors import InvalidId
from flask import Blueprint, render_template, request, redirect, url_for, session, flash, abort, current_app
from werkzeug.utils import secure_filename

from app.database import get_db
from database.seed_data import BANDERAS, url_bandera
from database.create_collections import ADMIN_USUARIO

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")

# ---------------------------------------------------------------------------
# Subida de imagenes: permite elegir un archivo de la computadora en vez de
# tener que pegar una URL. El archivo se guarda dentro de
# app/static/uploads/<coleccion>/ y en la base solo se guarda la ruta
# (ej. /static/uploads/jugadores/abc123.jpg).
#
# Importante (plan gratuito de Render): el disco no es permanente. Las
# imagenes subidas se conservan mientras el servicio siga corriendo, pero se
# pueden perder si se vuelve a desplegar la app (nuevo "git push"). Para
# fotos que quieras que nunca se borren, sigue usando una URL de internet.
# ---------------------------------------------------------------------------
EXTENSIONES_PERMITIDAS = {"png", "jpg", "jpeg", "gif", "webp"}


def _extension_valida(nombre_archivo):
    return "." in nombre_archivo and nombre_archivo.rsplit(".", 1)[1].lower() in EXTENSIONES_PERMITIDAS


def _guardar_imagen(slug, archivo):
    """Guarda el archivo subido y regresa la URL publica para guardarla en Mongo."""
    if not archivo or not archivo.filename:
        return None
    if not _extension_valida(archivo.filename):
        flash("Ese tipo de archivo no es una imagen valida (usa jpg, jpeg, png, gif o webp).")
        return None

    extension = archivo.filename.rsplit(".", 1)[1].lower()
    nombre_seguro = f"{uuid.uuid4().hex}.{extension}"

    carpeta = os.path.join(current_app.static_folder, "uploads", slug)
    os.makedirs(carpeta, exist_ok=True)
    archivo.save(os.path.join(carpeta, nombre_seguro))

    return f"/static/uploads/{slug}/{nombre_seguro}"


# ---------------------------------------------------------------------------
# Control de acceso: solo usuarios con es_admin = True
# ---------------------------------------------------------------------------
def admin_requerido(vista):
    @wraps(vista)
    def envoltura(*args, **kwargs):
        if not session.get("usuario_id"):
            flash("Inicia sesion para entrar al panel de administrador.")
            return redirect(url_for("auth.login"))

        db = get_db()
        try:
            usuario = db.usuarios.find_one({"_id": ObjectId(session["usuario_id"])})
        except InvalidId:
            usuario = None

        if not usuario or not usuario.get("es_admin", False):
            abort(403)

        return vista(*args, **kwargs)
    return envoltura


# ---------------------------------------------------------------------------
# Definicion de que coleccion se puede administrar y con que campos.
# tipo: "text" | "int" | "bool" | "lista" (texto separado por comas)
# ---------------------------------------------------------------------------
COLECCIONES = {
    "selecciones": {
        "titulo": "Selecciones",
        "icono": "🌎",
        "orden": [("nombre", 1)],
        "columnas": ["nombre", "grupo", "confederacion"],
        "campos": [
            ("nombre", "Nombre de la seleccion", "text", True),
            ("grupo", "Grupo (A-L)", "text", True),
            ("confederacion", "Confederacion", "text", False),
            ("bandera", "Bandera (emoji, opcional)", "text", False),
            ("bandera_url", "Imagen de la bandera (opcional, se autocompleta si la dejas vacia)", "imagen", False),
            ("favorito", "Marcar como favorito", "bool", False),
        ],
    },
    "jugadores": {
        "titulo": "Jugadores",
        "icono": "👤",
        "orden": [("nombre", 1)],
        "columnas": ["nombre", "seleccion", "posicion", "numero"],
        "campos": [
            ("nombre", "Nombre completo", "text", True),
            ("seleccion", "Seleccion", "text", True),
            ("posicion", "Posicion", "text", False),
            ("numero", "Numero", "int", False),
            ("edad", "Edad", "int", False),
            ("destacado", "Jugador destacado", "bool", False),
            ("foto_url", "Foto del jugador (opcional)", "imagen", False),
        ],
    },
    "partidos": {
        "titulo": "Partidos",
        "icono": "⚽",
        "orden": [("fecha", 1), ("hora", 1)],
        "columnas": ["fecha", "hora", "local", "visitante", "marcador"],
        "campos": [
            ("fecha", "Fecha (AAAA-MM-DD)", "text", True),
            ("hora", "Hora (HH:MM)", "text", False),
            ("fase", "Fase / Grupo", "text", False),
            ("local", "Equipo local", "text", True),
            ("visitante", "Equipo visitante", "text", True),
            ("estadio", "Estadio", "text", False),
            ("marcador", "Marcador (ej. 2-1, vacio si no se ha jugado)", "text", False),
        ],
    },
    "estadios": {
        "titulo": "Estadios",
        "icono": "🏟️",
        "orden": [("ciudad", 1)],
        "columnas": ["nombre", "ciudad", "pais", "capacidad"],
        "campos": [
            ("nombre", "Nombre del estadio", "text", True),
            ("ciudad", "Ciudad", "text", True),
            ("pais", "Pais", "text", True),
            ("capacidad", "Capacidad (numero, opcional)", "int", False),
        ],
    },
    "ciudades_sede": {
        "titulo": "Ciudades sede",
        "icono": "🏙️",
        "orden": [("num", 1)],
        "columnas": ["num", "ciudad", "pais", "estadio"],
        "campos": [
            ("num", "Numero", "int", False),
            ("pais", "Pais", "text", True),
            ("ciudad", "Ciudad", "text", True),
            ("estadio", "Estadio", "text", True),
            ("capacidad", "Capacidad (numero, opcional)", "int", False),
        ],
    },
    "historia_mundial": {
        "titulo": "Historia del Mundial",
        "icono": "🏆",
        "orden": [("anio", -1)],
        "columnas": ["anio", "campeon"],
        "campos": [
            ("anio", "Anio", "int", True),
            ("campeon", "Pais campeon", "text", True),
        ],
    },
    "noticias": {
        "titulo": "Noticias",
        "icono": "📰",
        "orden": [("horas", 1)],
        "columnas": ["titulo", "categoria", "horas"],
        "campos": [
            ("titulo", "Titulo", "text", True),
            ("categoria", "Categoria", "text", False),
            ("horas", "Horas desde publicada", "int", False),
        ],
    },
    "quiz_preguntas": {
        "titulo": "Preguntas del Quiz",
        "icono": "❓",
        "orden": [],
        "columnas": ["pregunta", "respuesta"],
        "campos": [
            ("pregunta", "Pregunta", "text", True),
            ("opciones", "Opciones (separadas por coma)", "lista", True),
            ("respuesta", "Respuesta correcta (debe ser igual a una opcion)", "text", True),
        ],
    },
    "anfitriones": {
        "titulo": "Paises anfitriones",
        "icono": "🌐",
        "orden": [],
        "columnas": ["pais", "codigo"],
        "campos": [
            ("pais", "Pais", "text", True),
            ("codigo", "Codigo ISO (2 letras)", "text", False),
            ("ciudades_sede", "Ciudades sede (separadas por coma)", "lista", False),
        ],
    },
}


def _coleccion_o_404(slug):
    config = COLECCIONES.get(slug)
    if not config:
        abort(404)
    return config


def _leer_formulario(slug, config, documento_actual=None):
    """Convierte los datos del formulario POST en un documento listo para Mongo."""
    doc = {}
    for nombre, _etiqueta, tipo, _requerido in config["campos"]:
        if tipo == "bool":
            doc[nombre] = request.form.get(nombre) == "on"
        elif tipo == "int":
            valor = request.form.get(nombre, "").strip()
            doc[nombre] = int(valor) if valor else None
        elif tipo == "lista":
            valor = request.form.get(nombre, "")
            doc[nombre] = [v.strip() for v in valor.split(",") if v.strip()]
        elif tipo == "imagen":
            archivo = request.files.get(nombre)
            url_nueva = _guardar_imagen(slug, archivo)
            if url_nueva:
                doc[nombre] = url_nueva
            elif documento_actual and documento_actual.get(nombre):
                # No se subio un archivo nuevo: conserva la imagen que ya tenia.
                doc[nombre] = documento_actual.get(nombre)
            else:
                doc[nombre] = ""
        else:
            doc[nombre] = request.form.get(nombre, "").strip()
    return doc


def _autocompletar_banderas(slug, doc):
    """Rellena los campos de bandera automaticamente segun el nombre del equipo/pais."""
    if slug == "selecciones":
        nombre = doc.get("nombre", "")
        if not doc.get("bandera"):
            doc["bandera"] = BANDERAS.get(nombre, "🏳️")
        if not doc.get("bandera_url"):
            doc["bandera_url"] = url_bandera(nombre)
    elif slug == "partidos":
        doc["bandera_local"] = BANDERAS.get(doc.get("local", ""), "🏳️")
        doc["bandera_visitante"] = BANDERAS.get(doc.get("visitante", ""), "🏳️")
        doc["bandera_local_url"] = url_bandera(doc.get("local", ""))
        doc["bandera_visitante_url"] = url_bandera(doc.get("visitante", ""))
        if not doc.get("marcador"):
            doc["marcador"] = None
    elif slug == "historia_mundial":
        campeon = doc.get("campeon", "")
        doc["bandera"] = BANDERAS.get(campeon, "🏳️")
        doc["bandera_url"] = url_bandera(campeon)
    return doc


# ---------------------------------------------------------------------------
# Panel principal
# ---------------------------------------------------------------------------
@admin_bp.route("/")
@admin_requerido
def dashboard():
    db = get_db()
    secciones = []
    for slug, config in COLECCIONES.items():
        secciones.append({
            "slug": slug,
            "titulo": config["titulo"],
            "icono": config["icono"],
            "total": db[slug].count_documents({}),
        })
    total_usuarios = db.usuarios.count_documents({})
    return render_template("admin/dashboard.html", secciones=secciones, total_usuarios=total_usuarios)


# ---------------------------------------------------------------------------
# Listado generico
# ---------------------------------------------------------------------------
@admin_bp.route("/<slug>")
@admin_requerido
def lista(slug):
    config = _coleccion_o_404(slug)
    db = get_db()
    cursor = db[slug].find()
    if config["orden"]:
        cursor = cursor.sort(config["orden"])
    documentos = list(cursor)
    for d in documentos:
        d["_id_str"] = str(d["_id"])

    etiquetas = {campo: etiqueta for campo, etiqueta, _tipo, _req in config["campos"]}
    columnas_info = [(campo, etiquetas.get(campo, campo)) for campo in config["columnas"]]

    return render_template("admin/lista.html", slug=slug, config=config,
                            documentos=documentos, columnas_info=columnas_info)


# ---------------------------------------------------------------------------
# Crear
# ---------------------------------------------------------------------------
@admin_bp.route("/<slug>/nuevo", methods=["GET", "POST"])
@admin_requerido
def nuevo(slug):
    config = _coleccion_o_404(slug)
    db = get_db()

    if request.method == "POST":
        doc = _leer_formulario(slug, config)
        doc = _autocompletar_banderas(slug, doc)
        db[slug].insert_one(doc)
        flash(f"Se agrego un nuevo registro en {config['titulo']}.")
        return redirect(url_for("admin.lista", slug=slug))

    return render_template("admin/formulario.html", slug=slug, config=config, documento=None, accion="nuevo")


# ---------------------------------------------------------------------------
# Editar
# ---------------------------------------------------------------------------
@admin_bp.route("/<slug>/editar/<doc_id>", methods=["GET", "POST"])
@admin_requerido
def editar(slug, doc_id):
    config = _coleccion_o_404(slug)
    db = get_db()
    try:
        oid = ObjectId(doc_id)
    except InvalidId:
        abort(404)

    if request.method == "POST":
        documento_actual = db[slug].find_one({"_id": oid})
        doc = _leer_formulario(slug, config, documento_actual=documento_actual)
        doc = _autocompletar_banderas(slug, doc)
        db[slug].update_one({"_id": oid}, {"$set": doc})
        flash(f"Registro actualizado en {config['titulo']}.")
        return redirect(url_for("admin.lista", slug=slug))

    documento = db[slug].find_one({"_id": oid})
    if not documento:
        abort(404)
    return render_template("admin/formulario.html", slug=slug, config=config, documento=documento, accion="editar")


# ---------------------------------------------------------------------------
# Eliminar
# ---------------------------------------------------------------------------
@admin_bp.route("/<slug>/eliminar/<doc_id>", methods=["POST"])
@admin_requerido
def eliminar(slug, doc_id):
    config = _coleccion_o_404(slug)
    db = get_db()
    try:
        oid = ObjectId(doc_id)
    except InvalidId:
        abort(404)
    db[slug].delete_one({"_id": oid})
    flash(f"Registro eliminado de {config['titulo']}.")
    return redirect(url_for("admin.lista", slug=slug))


# ---------------------------------------------------------------------------
# Grupos: editor especial de la tabla de posiciones (estadisticas por equipo)
# ---------------------------------------------------------------------------
@admin_bp.route("/grupos", methods=["GET"])
@admin_requerido
def grupos():
    db = get_db()
    grupos = list(db.grupos.find().sort("grupo", 1))
    return render_template("admin/grupos.html", grupos=grupos)


@admin_bp.route("/grupos/<letra>/guardar", methods=["POST"])
@admin_requerido
def guardar_grupo(letra):
    db = get_db()
    grupo_doc = db.grupos.find_one({"grupo": letra.upper()})
    if not grupo_doc:
        abort(404)

    nueva_tabla = []
    for fila in grupo_doc.get("tabla", []):
        seleccion = fila["seleccion"]
        prefijo = f"{seleccion}_"

        def num(campo, por_defecto=0):
            valor = request.form.get(prefijo + campo, "")
            return int(valor) if valor.strip() else por_defecto

        fila_nueva = dict(fila)
        fila_nueva.update({
            "pj": num("pj"), "pg": num("pg"), "pe": num("pe"), "pp": num("pp"),
            "gf": num("gf"), "gc": num("gc"), "pts": num("pts"),
        })
        nueva_tabla.append(fila_nueva)

    # Reordenar por puntos (de mayor a menor) y actualizar la posicion
    nueva_tabla.sort(key=lambda f: f["pts"], reverse=True)
    for i, fila in enumerate(nueva_tabla, start=1):
        fila["posicion"] = i

    db.grupos.update_one({"_id": grupo_doc["_id"]}, {"$set": {"tabla": nueva_tabla}})
    flash(f"Tabla del Grupo {letra.upper()} actualizada.")
    return redirect(url_for("admin.grupos"))


# ---------------------------------------------------------------------------
# Usuarios: consulta y otorgar / quitar el rol de administrador
# ---------------------------------------------------------------------------
@admin_bp.route("/usuarios")
@admin_requerido
def usuarios():
    db = get_db()
    usuarios = list(db.usuarios.find().sort("nombre", 1))
    for u in usuarios:
        u["_id_str"] = str(u["_id"])
    return render_template("admin/usuarios.html", usuarios=usuarios)


@admin_bp.route("/quiniela")
@admin_requerido
def quiniela_partidos():
    db = get_db()
    partidos = list(db.partidos.find().sort([("fecha", 1), ("hora", 1)]))
    for p in partidos:
        p["_id_str"] = str(p["_id"])
        p["total_predicciones"] = db.predicciones.count_documents({"partido_id": p["_id_str"]})
    return render_template("admin/quiniela_partidos.html", partidos=partidos)


@admin_bp.route("/quiniela/<partido_id>", methods=["GET", "POST"])
@admin_requerido
def quiniela_predicciones(partido_id):
    db = get_db()
    try:
        oid = ObjectId(partido_id)
    except InvalidId:
        abort(404)
    partido = db.partidos.find_one({"_id": oid})
    if not partido:
        abort(404)

    if request.method == "POST":
        predicciones = list(db.predicciones.find({"partido_id": partido_id}))
        for pred in predicciones:
            valor = request.form.get(f"estado_{pred['_id']}", "automatico")
            nuevo_estado = None if valor == "automatico" else valor
            db.predicciones.update_one({"_id": pred["_id"]}, {"$set": {"estado_manual": nuevo_estado}})
        flash(f"Se guardaron los resultados de {partido.get('local')} vs {partido.get('visitante')}.")
        return redirect(url_for("admin.quiniela_predicciones", partido_id=partido_id))

    predicciones = list(db.predicciones.find({"partido_id": partido_id}))
    ids_validos = [ObjectId(p["usuario_id"]) for p in predicciones if ObjectId.is_valid(p.get("usuario_id", ""))]
    usuarios_map = {str(u["_id"]): u for u in db.usuarios.find({"_id": {"$in": ids_validos}})}

    filas = []
    for pred in predicciones:
        usuario = usuarios_map.get(pred.get("usuario_id"))
        filas.append({
            "id": str(pred["_id"]),
            "usuario_nombre": usuario["nombre"] if usuario else "(usuario eliminado)",
            "prediccion": f'{pred["goles_local"]}-{pred["goles_visitante"]}',
            "estado_actual": pred.get("estado_manual") or "automatico",
        })

    return render_template("admin/quiniela_predicciones.html", partido=partido, filas=filas)


@admin_bp.route("/usuarios/<usuario_id>/admin/toggle", methods=["POST"])
@admin_requerido
def toggle_admin(usuario_id):
    db = get_db()
    try:
        oid = ObjectId(usuario_id)
    except InvalidId:
        abort(404)

    # No te puedes quitar el rol a ti mismo (para no quedarte afuera sin querer)
    if str(oid) == session.get("usuario_id"):
        flash("No puedes quitarte el rol de administrador a ti mismo.")
        return redirect(url_for("admin.usuarios"))

    usuario = db.usuarios.find_one({"_id": oid})
    if not usuario:
        abort(404)

    # El administrador fijo nunca se puede degradar desde aqui, para que
    # siempre quede al menos una cuenta con acceso al panel.
    if usuario.get("usuario") == ADMIN_USUARIO and usuario.get("es_admin", False):
        flash(f"'{ADMIN_USUARIO}' es el administrador fijo del sistema y no se le puede quitar el rol.")
        return redirect(url_for("admin.usuarios"))

    nuevo_valor = not usuario.get("es_admin", False)
    db.usuarios.update_one({"_id": oid}, {"$set": {"es_admin": nuevo_valor}})
    flash(f"{usuario['nombre']} ahora {'es' if nuevo_valor else 'ya no es'} administrador.")
    return redirect(url_for("admin.usuarios"))
