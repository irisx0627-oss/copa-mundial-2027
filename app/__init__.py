from flask import Flask
from app.config import Config


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Registrar cada bloque de pantallas (blueprint)
    from app.routes.auth import auth_bp
    from app.routes.main import main_bp
    from app.routes.content import content_bp
    from app.routes.extras import extras_bp
    from app.routes.quiniela import quiniela_bp
    from app.routes.admin import admin_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(content_bp)
    app.register_blueprint(extras_bp)
    app.register_blueprint(quiniela_bp)
    app.register_blueprint(admin_bp)

    return app
