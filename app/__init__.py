from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
import redis
import os

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
r = redis.from_url(os.getenv("REDIS_URL", "redis://redis:6379"))

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-super-secret')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    from .routes import auth, main
    from .print_routes import print_bp
    app.register_blueprint(auth)
    app.register_blueprint(main)
    app.register_blueprint(print_bp)

    return app