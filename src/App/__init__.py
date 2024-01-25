from flask import Flask
from App.Core.config import Config

from App.Admin import Module as AdminRoutes
from App.Mahasiswa import Module as MahasiswaRoutes
from App.Dosen import Module as DosenRoutes
from App.Auth import Module as AuthModule
from App.Extensions.routes import Routes
from flask_wtf import CSRFProtect
from App.Core.database import db
from App.Core.session import Session

app = Flask(__name__, static_folder="./Static/")
csrf = CSRFProtect(app)


def create_app(app, config_class=Config):
    app.config.from_object(config_class)
    app.secret_key = app.config['SECRET_KEY']
    Session(app)
    db.init_app(app)

    # Initialize Flask extensions here
    # Register blueprints here
    app.register_blueprint(AuthModule, url_prefix='/auth')
    app.register_blueprint(DosenRoutes, url_prefix='/dosen')
    app.register_blueprint(AdminRoutes, url_prefix='/admin')
    app.register_blueprint(MahasiswaRoutes, url_prefix='/mahasiswa')

    routes = Routes(app)

    routes.redirect('/', 'auth.login')

    return app
