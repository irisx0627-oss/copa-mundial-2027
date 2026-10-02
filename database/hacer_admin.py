# -*- coding: utf-8 -*-
"""
Convierte a un usuario ya registrado en administrador (es_admin = True).

Se usa UNA sola vez, para crear al primer administrador (despues de eso,
un administrador ya puede ascender a otras personas desde la app, en
Panel de administrador -> Usuarios, sin volver a tocar la terminal).

Como correrlo (con el entorno virtual activado, desde la raiz del proyecto):

    python database/hacer_admin.py tu_usuario_o_correo

Ejemplo:

    python database/hacer_admin.py iris@correo.com
    python database/hacer_admin.py iris
"""

import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import get_db, check_connection


def main():
    if len(sys.argv) < 2:
        print("Falta el usuario o correo. Uso:")
        print("    python database/hacer_admin.py tu_usuario_o_correo")
        return

    identificador = sys.argv[1].strip()

    print("Conectando a MongoDB Atlas...")
    ok, mensaje = check_connection()
    print(mensaje)
    if not ok:
        return

    db = get_db()
    usuario = db.usuarios.find_one({"$or": [{"correo": identificador.lower()}, {"usuario": identificador}]})

    if not usuario:
        print(f"No se encontro ninguna cuenta con usuario o correo '{identificador}'.")
        print("Registra la cuenta primero desde la app (pantalla Registrarse) y vuelve a correr este script.")
        return

    db.usuarios.update_one({"_id": usuario["_id"]}, {"$set": {"es_admin": True}})
    print(f"Listo. '{usuario['nombre']}' ({usuario['correo']}) ya es administrador.")
    print("Inicia sesion de nuevo en la app para que el cambio tome efecto en el menu de Ajustes.")


if __name__ == "__main__":
    main()
