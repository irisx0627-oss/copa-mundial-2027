import os
from dotenv import load_dotenv

# Carga las variables definidas en el archivo .env (que esta en la raiz del proyecto)
load_dotenv()


class Config:
    """Configuracion central de la aplicacion. Todo lo sensible sale del .env,
    nunca se escribe directo en el codigo."""

    SECRET_KEY = os.environ.get("SECRET_KEY", "clave-temporal-solo-para-desarrollo")

    MONGO_URI = os.environ.get("MONGO_URI", "")
    MONGO_DB_NAME = os.environ.get("MONGO_DB_NAME", "copa_mundial_2027")

    APP_NAME = "Copa Mundial 2027"
