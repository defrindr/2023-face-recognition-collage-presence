from flask import render_template
from App.Auth.auth_session import loggedInUser

def index():
    user = loggedInUser()
    return render_template("Mahasiswa/index.html", user=user)