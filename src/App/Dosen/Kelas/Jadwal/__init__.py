from . import controller
from App.Extensions.routes import Routes
from flask import Blueprint

Module = Blueprint('jadwal', __name__, template_folder="/Jadwal")
registerRoute = Routes(Module)

registerRoute.get("/<kelas>", controller.index)
registerRoute.get("/create/<kelas>", controller.create)
registerRoute.post("/store/<kelas>", controller.store)
registerRoute.post("/destroy/<kelas>/<id>", controller.destroy)
registerRoute.post("/buka-presensi/<kelas>/<id>", controller.bukaPresensi)
registerRoute.post("/tutup-presensi/<kelas>/<id>", controller.tutupPresensi)
