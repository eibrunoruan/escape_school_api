from flask import Flask, jsonify
from flask_migrate import Migrate
from config import Config
from app.db import db
from app.routes import main_bp, game_data_bp
from app.routes.auth import auth_bp # Importe o novo auth_bp

migrate = Migrate()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    app.config['SECRET_KEY'] = 'secret'

    db.init_app(app)
    migrate.init_app(app, db)

    app.register_blueprint(main_bp)
    app.register_blueprint(game_data_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth') # Registre o auth_bp com o prefixo /auth

    @app.errorhandler(400)
    def bad_request(e):
        return jsonify(error=str(e)), 400
    @app.errorhandler(401)
    def unauthorized(e):
        return jsonify(error=str(e)), 401
    @app.errorhandler(404)
    def not_found(e):
        return jsonify(error=str(e)), 404
    @app.errorhandler(500)
    def internal_server_error(e):
        return jsonify(error=str(e)), 500
    @app.errorhandler(503)
    def service_unavailable(e):
        return jsonify(error=str(e)), 503

    return app