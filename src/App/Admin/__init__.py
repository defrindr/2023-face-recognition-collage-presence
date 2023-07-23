from . import controller
from App.Admin.middleware import CheckIsLoggedAdmin
from App.Extensions.routes import Routes
from App.Admin.Mahasiswa import Module as AdminMahasiswaModule
from flask import Blueprint

Module = Blueprint('admin', __name__, template_folder="../Templates/Admin")

registerRoute = Routes(Module)

registerRoute.middleware(CheckIsLoggedAdmin)
registerRoute.get("/", controller.index)

Module.register_blueprint(AdminMahasiswaModule, url_prefix="/mahasiswa")
