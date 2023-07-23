from . import controller
from App.Admin.middleware import CheckIsLoggedAdmin
from App.Extensions.routes import Routes
from App.Admin.Mahasiswa import Module as MahasiswaAdminModule
from App.Admin.MataKuliah import Module as MatakuliahAdminModule
from App.Admin.Kelas import Module as KelasAdminModule
from flask import Blueprint

Module = Blueprint('admin', __name__, template_folder="../Templates/Admin")

registerRoute = Routes(Module)

registerRoute.middleware(CheckIsLoggedAdmin)
registerRoute.get("/", controller.index)

Module.register_blueprint(MahasiswaAdminModule, url_prefix="/mahasiswa")
Module.register_blueprint(KelasAdminModule, url_prefix="/kelas")
Module.register_blueprint(MatakuliahAdminModule, url_prefix="/mata-kuliah")
