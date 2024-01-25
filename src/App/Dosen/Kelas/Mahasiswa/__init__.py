from . import controller
from App.Extensions.routes import Routes
from flask import Blueprint

Module = Blueprint('mahasiswa', __name__, template_folder="/Mahasiswa")
registerRoute = Routes(Module)

registerRoute.get("/<kelas>", controller.index)
registerRoute.get("/create/<kelas>", controller.create)
registerRoute.post("/store/<kelas>", controller.store)
registerRoute.post("/destroy/<kelas>/<id>", controller.destroy)
