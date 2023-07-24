from App.Auth.auth_session import SESS_AUTH_ROLE, getSessionAuth
from App.Models.User import Role
from flask import abort


def CheckIsLoggedMahasiswa():
    session = getSessionAuth()
    if (session[SESS_AUTH_ROLE] != Role.MAHASISWA):
        return abort(403)
    
