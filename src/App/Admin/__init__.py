from . import controller
from App.Admin.middleware import CheckIsLoggedAdmin
from App.Extensions.routes import Routes
from App.Admin.Admin import Module as AdminAdminModule
from App.Admin.Mahasiswa import Module as MahasiswaAdminModule
from App.Admin.MataKuliah import Module as MatakuliahAdminModule
from App.Admin.Report import Module as ReportAdminModule
from App.Admin.Kelas import Module as KelasAdminModule
from flask import Blueprint, render_template

Module = Blueprint('admin', __name__, template_folder="../Templates/Admin")

registerRoute = Routes(Module)

registerRoute.middleware(CheckIsLoggedAdmin)
registerRoute.get("/", controller.index)

Module.register_blueprint(AdminAdminModule, url_prefix="/admin")
Module.register_blueprint(MahasiswaAdminModule, url_prefix="/mahasiswa")
Module.register_blueprint(KelasAdminModule, url_prefix="/kelas")
Module.register_blueprint(MatakuliahAdminModule, url_prefix="/mata-kuliah")
Module.register_blueprint(ReportAdminModule, url_prefix="/report")


# @Module.errorhandler(Exception)
# def handle_exception(e):
#     # Return a user-friendly error message
#     if hasattr(e, "code"):
#         code = e.code
#     else:
#         code = 500
#     return render_template('error_generic.html', message=str(e), code=code), code
