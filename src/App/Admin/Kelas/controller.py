from flask import render_template, request, url_for, flash, redirect
from sqlalchemy import or_
from App.Admin import MataKuliah
from App.Core.database import db
from App.Models import Kelas
from App.Models.Kelas import _baseQuery, _fetchById, Kelas as KelasModel, _getListFakultas, _getListProdi

module = "admin.kelas"
template = 'Kelas/'


def index():

    title = "Management Kelas"
    headers = ['No', 'Fakultas', 'Prodi', 'Kelas', 'Aksi']

    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    search = request.args.get('search', '', type=str)

    baseQuery = _baseQuery()

    if search != '':
        baseQuery = baseQuery.filter(
            or_(
                KelasModel.prodi.like(f"%{search}%"),
                KelasModel.fakultas.like(f"%{search}%"),
                KelasModel.kelas.like(f"%{search}%")
            )
        )
        pass

    total_data = baseQuery.count()
    pagination = baseQuery.paginate(page=page, per_page=per_page)
    start_data = page * per_page - per_page
    len_items = len(pagination.items)
    return render_template(template + 'index.html', pagination=pagination, len_items=len_items, headers=headers, title=title, module=module, start_data=start_data, per_page=per_page, total_data=total_data, search=search)


def create():
    title = "Tambah Kelas"
    fakultas = _getListFakultas()
    prodi = _getListProdi()
    return render_template(template + 'create.html', title=title, module=module, fakultas=fakultas, prodi=prodi)


def store():
    # validation
    required_fields = ['fakultas', 'kelas', 'prodi']
    form = request.form
    for field in required_fields:
        if (form[field] is None):
            flash('Terjadi kesalahan saat menambahkan data', 'danger')
            return redirect(url_for(f'{module}.create'))

    # save model
    model = KelasModel(
        fakultas=form['fakultas'],
        kelas=form['kelas'],
        prodi=form['prodi'],
        flag=1
    )

    # commit
    db.session.add(model)
    db.session.commit()

    flash('Data telah ditambahkan', 'info')
    return redirect(url_for(f'{module}.index'))


def edit(id):
    title = "Edit Kelas"
    model = _fetchById(id)
    fakultas = _getListFakultas()
    prodi = _getListProdi()
    return render_template(template + 'edit.html', title=title, module=module, model=model, fakultas=fakultas, prodi=prodi)


def update(id):
    form = request.form
    form_keys = form.keys()
    model = _fetchById(id)

    if "fakultas" in form_keys:
        model.fakultas = form['fakultas']
    if "prodi" in form_keys:
        model.prodi = form['prodi']
    if "kelas" in form_keys:
        model.kelas = form['kelas']

    db.session.commit()
    flash('Data berhasil diubah', 'info')
    return redirect(url_for(f'{module}.index'))


def destroy(id):
    model = _fetchById(id)
    model.flag = 0
    db.session.commit()
    flash('Data berhasil diubah', 'info')
    return redirect(url_for(f'{module}.index'))
