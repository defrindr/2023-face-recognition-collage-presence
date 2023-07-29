import os
from flask import jsonify, render_template, request, url_for, flash, redirect, abort

from App.Auth.auth_session import loggedInUser
from facerec import predict_face

from .service import _getKelas, _indexService, _presensiVideo
from flask import Flask, render_template, Response
import cv2

module = "mahasiswa.jadwal"
template = 'Mahasiswa/Jadwal/'

face_detected = ""


def index():
    user_login = loggedInUser()
    if user_login is None:
        return abort(403)

    kelas = user_login.anggota_kelas
    if user_login is None:
        flash('kelas belum diatur')
        return redirect(url_for('mahasiswa.index'))

    kelas = kelas[0].kelas_id
    kelas_model = _getKelas(kelas)
    if kelas_model is None:
        return abort(404)

    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    search = request.args.get('search', '', type=str)

    total_data, pagination, start_data, len_items, title, headers = _indexService(
        page=page,
        per_page=per_page,
        search=search,
        kelas=kelas_model
    )

    return render_template(
        template + 'index.html',
        pagination=pagination,
        len_items=len_items,
        headers=headers,
        title=title,
        module=module,
        start_data=start_data,
        per_page=per_page,
        total_data=total_data,
        search=search,
        kelas=kelas,
        user_login = user_login,
    )


def presensiVideo():
    return _presensiVideo(request)
