from . import controller
from App.Dosen.middleware import CheckIsLoggedDosen
from App.Extensions.routes import Routes
from App.Dosen.Report import Module as ReportAdminModule
from App.Dosen.Kelas import Module as KelasAdminModule
from flask import Blueprint, render_template

Module = Blueprint('dosen', __name__, template_folder="../Templates/Dosen")

registerRoute = Routes(Module)

registerRoute.middleware(CheckIsLoggedDosen)
registerRoute.get("/", controller.index)

Module.register_blueprint(KelasAdminModule, url_prefix="/kelas")
Module.register_blueprint(ReportAdminModule, url_prefix="/report")


# @Module.errorhandler(Exception)
# def handle_exception(e):
#     # Return a user-friendly error message
#     if hasattr(e, "code"):
#         code = e.code
#     else:
#         code = 500
#     return render_template('error_generic.html', message=str(e), code=code), code
