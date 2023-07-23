from . import controller
from .Mahasiswa import Module as MahasiswaKelasAdminModule
from App.Extensions.routes import Routes
from flask import Blueprint

Module = Blueprint('kelas', __name__, template_folder="/Kelas")

Module.register_blueprint(MahasiswaKelasAdminModule, url_prefix='/mahasiswa')

registerRoute = Routes(Module)

registerRoute.get("/", controller.index)
registerRoute.get("/create", controller.create)
registerRoute.post("/store", controller.store)
registerRoute.get("/edit/<id>", controller.edit)
registerRoute.post("/update/<id>", controller.update)
registerRoute.post("/destroy/<id>", controller.destroy)
