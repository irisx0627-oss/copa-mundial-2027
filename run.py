"""
Punto de entrada de la aplicacion.

En Visual Studio Code: clic derecho -> "Run Python File", o F5,
o desde la terminal:  python run.py

La app abre en: http://127.0.0.1:5000
"""

from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
