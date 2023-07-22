from App.Admin import controller
from App.Admin.middleware import CheckIsLoggedAdmin
from App.Extensions.routes import Routes
from flask import Blueprint

Module = Blueprint('admin', __name__)
registerRoute = Routes(Module)


registerRoute.middleware(CheckIsLoggedAdmin)
registerRoute.get("/", controller.index)
