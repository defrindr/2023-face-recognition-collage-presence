import io
import os
from tempfile import TemporaryDirectory
import cv2
from flask import jsonify, render_template, request, url_for, flash, redirect
from sqlalchemy import or_

from App.Models.User import Role, User, _baseQuery, _fetchById, _fetchByUsername, _hashPassword
from hashlib import md5
from App.Core.database import db
from facerec import training_data

module = "admin.mahasiswa"
template = 'Admin/Mahasiswa/'


def index():

    title = "Management Mahasiswa"
    headers = ['No', 'NIM', 'Name', 'Aksi']

    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    search = request.args.get('search', '', type=str)

    baseQuery = _baseQuery()

    if search != '':
        baseQuery = baseQuery.filter(
            or_(
                User.username.like(f"%{search}%"),
                User.name.like(f"%{search}%")
            )
        )
        pass

    total_data = baseQuery.count()
    pagination = baseQuery.paginate(page=page, per_page=per_page)
    start_data = page * per_page - per_page
    len_items = len(pagination.items)
    return render_template(template + 'index.html', pagination=pagination, len_items=len_items, headers=headers, title=title, module=module, start_data=start_data, per_page=per_page, total_data=total_data, search=search)


def create():
    title = "Tambah Mahasiswa"
    return render_template(template + 'create.html', title=title, module=module)


def store():
    # validation
    required_fields = ['nim', 'name', 'password']
    form = request.form
    for field in required_fields:
        if (form[field] is None):
            flash('Terjadi kesalahan saat menambahkan data', 'danger')
            return redirect(url_for(f'{module}.create'))

    # check if duplicate
    exist = _fetchByUsername(form['nim'])
    if exist is not None:
        flash('Data telah ditambahkan sebelumnya', 'danger')
        return redirect(url_for(f'{module}.create'))

    # save model
    model = User(
        username=form['nim'],
        name=form['name'],
        role=Role.MAHASISWA,
        password=_hashPassword(form['password']),
        flag=1
    )

    # commit
    db.session.add(model)
    db.session.commit()

    flash('Data telah ditambahkan', 'info')
    return redirect(url_for(f'{module}.index'))


def edit(id):
    title = "Edit Mahasiswa"
    model = _fetchById(id)
    return render_template(template + 'edit.html', title=title, module=module, model=model)


def update(id):
    form = request.form
    form_keys = form.keys()
    model = _fetchById(id)

    if "nim" in form_keys:
        model.username = form['nim']
    if "name" in form_keys:
        model.name = form['name']
    if "password" in form_keys:
        model.password = _hashPassword(form['password'])

    db.session.commit()
    flash('Data berhasil diubah', 'info')
    return redirect(url_for(f'{module}.index'))


def destroy(id):
    model = _fetchById(id)
    model.flag = 0
    db.session.commit()
    flash('Data berhasil diubah', 'info')
    return redirect(url_for(f'{module}.index'))


def trainingVideo():
    base_dir = "facerec/training/"
    temp_dir = f"{base_dir}/temp"
    face_dir = f"{base_dir}/faces"
    temp_video_path = temp_dir+'/video.mp4'

    face_label = request.form['face_label']
    path_training = f"{face_dir}/{face_label}/"

    # Check if 'faces' directory exists, if not, create one
    if not os.path.exists(path_training):
        os.makedirs(path_training)

    # Check if 'temp' directory exists, if not, create one
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)

    # save video
    video = request.files['video']
    video.save(temp_video_path)
    training_data(temp_video_path, face_label)

    return jsonify({'message': 'Video processed successfully!'})
