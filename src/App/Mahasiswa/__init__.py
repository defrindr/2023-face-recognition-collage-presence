from App.Extensions.routes import Routes
from flask import Blueprint, render_template
from .Jadwal import Module as JadwalMahasiswaModule
from App.Mahasiswa.middleware import CheckIsLoggedMahasiswa
from . import controller

Module = Blueprint('mahasiswa', __name__, template_folder="../Templates/Mahasiswa")

Module.register_blueprint(JadwalMahasiswaModule, url_prefix="/jadwal")

registerRoute = Routes(Module)

registerRoute.middleware(CheckIsLoggedMahasiswa)
registerRoute.get("/", controller.index)


@Module.errorhandler(Exception)
def handle_exception(e):
    # Return a user-friendly error message
    if hasattr(e, "code"):
        code = e.code
    else:
        code = 500
    return render_template('Mahasiswa/error_generic.html', message=str(e), code=code), code
