# -*- coding: utf-8 -*-
"""
Script para crear las colecciones en MongoDB Atlas y cargarlas con la
informacion del Mundial 2026.

COMO EJECUTARLO DESDE VISUAL STUDIO CODE:
1. Abre la carpeta "CopaMundial2027" en VS Code.
2. Crea tu entorno virtual (una sola vez):
       python -m venv venv
       venv\\Scripts\\activate        (Windows)
       source venv/bin/activate       (Mac/Linux)
3. Instala dependencias:
       pip install -r requirements.txt
4. Copia .env.example a .env y pega tu cadena de conexion de MongoDB Atlas
   en MONGO_URI.
5. Corre este archivo (clic derecho -> "Run Python File" o F5, o:
       python database/create_collections.py
6. Veras en consola cuantos documentos se insertaron en cada coleccion.

Este script se puede ejecutar las veces que quieras: primero borra los datos
viejos de cada coleccion (drop) y los vuelve a crear, para que nunca queden
duplicados.
"""

import os
import sys
from datetime import datetime

# Permite ejecutar este archivo directamente (python database/create_collections.py)
# sin errores de import, sin importar desde donde se llame.
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from werkzeug.security import generate_password_hash

from app.database import get_db, check_connection
from database import seed_data as data

# ---------------------------------------------------------------------------
# Administrador fijo: esta cuenta siempre existe para poder entrar al panel
# de administrador (/admin) sin tener que registrar y luego promover a nadie.
# Puedes cambiar estos valores poniendo ADMIN_USUARIO / ADMIN_CORREO /
# ADMIN_CONTRASENA en tu archivo .env; si no los pones, se usan estos por
# defecto. *** Cambia la contraseña despues de tu primer inicio de sesion
# (Ajustes -> Perfil) o definela tu mismo en el .env antes de correr esto. ***
# ---------------------------------------------------------------------------
ADMIN_USUARIO = os.environ.get("ADMIN_USUARIO", "admin")
ADMIN_CORREO = os.environ.get("ADMIN_CORREO", "admin@copamundial2027.com")
ADMIN_CONTRASENA = os.environ.get("ADMIN_CONTRASENA", "Mundial2027!")
ADMIN_NOMBRE = os.environ.get("ADMIN_NOMBRE", "Administrador")


def crear_indices(db):
    """Crea indices utiles (por ejemplo, que no se repita el usuario o el correo)."""
    db.usuarios.create_index("correo", unique=True)
    db.usuarios.create_index("usuario", unique=True)
    db.selecciones.create_index("nombre", unique=True)
    db.grupos.create_index("grupo", unique=True)
    print("  -> Indices creados (correo/usuario unicos, seleccion/grupo unicos).")


def cargar_coleccion(db, nombre_coleccion, documentos):
    """Borra la coleccion si existia y la vuelve a llenar desde cero."""
    coleccion = db[nombre_coleccion]
    coleccion.drop()
    if documentos:
        coleccion.insert_many(documentos)
    print(f"  -> Coleccion '{nombre_coleccion}': {len(documentos)} documentos insertados.")


def asegurar_admin_fijo(db):
    """
    Garantiza que siempre exista una cuenta de administrador, sin importar
    cuantas veces se corra este script. Si la cuenta no existe, la crea; si
    ya existe (por ejemplo porque ya le cambiaste la contraseña desde la
    app), solo nos aseguramos de que su rol siga siendo administrador, sin
    tocar su contraseña ni sus demas datos.
    """
    existente = db.usuarios.find_one({"usuario": ADMIN_USUARIO})

    if existente:
        if not existente.get("es_admin"):
            db.usuarios.update_one({"_id": existente["_id"]}, {"$set": {"es_admin": True}})
        print(f"  -> Administrador fijo '{ADMIN_USUARIO}' ya existia (se conserva su contraseña actual).")
        return

    db.usuarios.insert_one({
        "nombre": ADMIN_NOMBRE,
        "correo": ADMIN_CORREO,
        "usuario": ADMIN_USUARIO,
        "contrasena_hash": generate_password_hash(ADMIN_CONTRASENA),
        "fecha_nacimiento": "1990-01-01",
        "creado_en": datetime.utcnow(),
        "notificaciones_activadas": True,
        "idioma": "es",
        "tema": "oscuro",
        "es_admin": True,
    })
    print(f"  -> Administrador fijo creado -> usuario: '{ADMIN_USUARIO}'  contraseña: '{ADMIN_CONTRASENA}'")
    print("     (Cambiala despues de tu primer inicio de sesion, en Ajustes -> Perfil.)")


def main():
    print("Conectando a MongoDB Atlas...")
    ok, mensaje = check_connection()
    print(mensaje)
    if not ok:
        print("\nRevisa tu archivo .env (MONGO_URI) y que tu IP este permitida en Atlas "
              "(Network Access -> Add IP Address).")
        return

    db = get_db()
    print(f"\nBase de datos seleccionada: {db.name}")
    print("Creando e insertando colecciones...\n")

    cargar_coleccion(db, "anfitriones", data.ANFITRIONES)
    cargar_coleccion(db, "ciudades_sede", data.CIUDADES_SEDE)
    cargar_coleccion(db, "estadios", data.ESTADIOS)
    cargar_coleccion(db, "selecciones", data.construir_selecciones())
    cargar_coleccion(db, "grupos", data.construir_grupos())
    cargar_coleccion(db, "jugadores", data.JUGADORES_DESTACADOS)
    cargar_coleccion(db, "partidos", data.PARTIDOS)
    cargar_coleccion(db, "historia_mundial", data.HISTORIA_MUNDIAL)
    cargar_coleccion(db, "noticias", data.NOTICIAS)
    cargar_coleccion(db, "quiz_preguntas", data.QUIZ_PREGUNTAS)
    cargar_coleccion(db, "datos_generales", [data.DATOS_GENERALES])

    # La coleccion de usuarios NO se borra: se llena cuando la gente se
    # registra en la app (pantalla "Registrarse"), y aqui solo garantizamos
    # que exista y que la cuenta fija de administrador este presente.
    if "usuarios" not in db.list_collection_names():
        db.create_collection("usuarios")
    print("  -> Coleccion 'usuarios' lista (se conserva entre ejecuciones).")

    asegurar_admin_fijo(db)

    # La coleccion de predicciones (quiniela) tambien se llena solo cuando la
    # gente pronostica marcadores. Aqui solo nos aseguramos de que exista.
    if "predicciones" not in db.list_collection_names():
        db.create_collection("predicciones")
    db.predicciones.create_index([("usuario_id", 1), ("partido_id", 1)], unique=True)
    print("  -> Coleccion 'predicciones' (quiniela) lista, con indice unico usuario+partido.")

    print("\nCreando indices...")
    crear_indices(db)

    print("\n¡Listo! Todas las colecciones fueron creadas y cargadas en Atlas.")
    print("Colecciones actuales en la base:", db.list_collection_names())


if __name__ == "__main__":
    main()
