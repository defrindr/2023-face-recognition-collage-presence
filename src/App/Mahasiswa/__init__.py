from App.Extensions.routes import Routes
from flask import Blueprint

from App.Mahasiswa.middleware import CheckIsLoggedMahasiswa
from . import controller

Module = Blueprint('mahasiswa', __name__)

registerRoute = Routes(Module)

registerRoute.middleware(CheckIsLoggedMahasiswa)
registerRoute.get("/", controller.index)