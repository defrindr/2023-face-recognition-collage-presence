from . import controller
from App.Extensions.routes import Routes
from flask import Blueprint

Module = Blueprint('report', __name__, template_folder="/Report")
registerRoute = Routes(Module)

registerRoute.get("/<id>/", controller.index)