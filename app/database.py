"""
Conexion a MongoDB Atlas.

Este modulo se encarga de crear UNA sola conexion reutilizable (patron singleton)
hacia tu base de datos en Atlas, para que el resto de la aplicacion (rutas,
scripts de carga, etc.) simplemente hagan: from app.database import get_db
"""

from pymongo import MongoClient
from pymongo.server_api import ServerApi
from app.config import Config

_client = None
_db = None


def get_client():
    """Devuelve el cliente de MongoDB (lo crea la primera vez que se pide)."""
    global _client
    if _client is None:
        if not Config.MONGO_URI:
            raise RuntimeError(
                "No configuraste MONGO_URI. Copia .env.example a .env y pon tu "
                "cadena de conexion de MongoDB Atlas."
            )
        _client = MongoClient(Config.MONGO_URI, server_api=ServerApi("1"))
    return _client


def get_db():
    """Devuelve la base de datos (copa_mundial_2027 por defecto)."""
    global _db
    if _db is None:
        _db = get_client()[Config.MONGO_DB_NAME]
    return _db


def check_connection():
    """Hace un ping a Atlas para confirmar que la conexion sirve.
    Util para mostrar un mensaje claro en consola al arrancar la app."""
    try:
        get_client().admin.command("ping")
        return True, "Conexion exitosa a MongoDB Atlas."
    except Exception as e:
        return False, f"No se pudo conectar a MongoDB Atlas: {e}"
