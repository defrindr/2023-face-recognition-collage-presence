from . import controller
from App.Extensions.routes import Routes
from flask import Blueprint

Module = Blueprint('jadwal', __name__, template_folder="/Jadwal")
registerRoute = Routes(Module)

registerRoute.get("/", controller.index)
registerRoute.post("/presensi-video", controller.presensiVideo)
# registerRoute.get("/create", controller.create)
# registerRoute.post("/destroy/<id>", controller.destroy)
# registerRoute.post("/buka-presensi/<id>", controller.bukaPresensi)
# registerRoute.post("/tutup-presensi/<id>", controller.tutupPresensi)
