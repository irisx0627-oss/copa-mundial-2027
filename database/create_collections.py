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

# Permite ejecutar este archivo directamente (python database/create_collections.py)
# sin errores de import, sin importar desde donde se llame.
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import get_db, check_connection
from database import seed_data as data


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

    # La coleccion de usuarios se deja vacia; se llena cuando la gente se registra
    # en la app (pantalla "Registrarse"). Solo nos aseguramos de que exista.
    if "usuarios" not in db.list_collection_names():
        db.create_collection("usuarios")
    print("  -> Coleccion 'usuarios' lista (vacia, se llena con los registros).")

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
