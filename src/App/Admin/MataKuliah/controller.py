from flask import render_template, request, url_for, flash, redirect
from App.Admin import MataKuliah
from App.Core.database import db
from App.Models.MataKuliah import _baseQuery, _fetchById, _fetchByName, MataKuliah

module = "admin.matakuliah"
template = 'Admin/Mata Kuliah/'


def index():

    title = "Management Matkul"
    headers = ['No', 'Name', 'Aksi']

    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    search = request.args.get('search', '', type=str)

    baseQuery = _baseQuery()

    if search != '':
        baseQuery = baseQuery.filter(
            MataKuliah.nama.like(f"%{search}%")
        )
        pass

    total_data = baseQuery.count()
    pagination = baseQuery.paginate(page=page, per_page=per_page)
    start_data = page * per_page - per_page
    len_items = len(pagination.items)
    return render_template(template + 'index.html', pagination=pagination, len_items=len_items, headers=headers, title=title, module=module, start_data=start_data, per_page=per_page, total_data=total_data, search=search)


def create():
    title = "Tambah Matkul"
    return render_template(template + 'create.html', title=title, module=module)


def store():
    # validation
    required_fields = ['nama']
    form = request.form
    for field in required_fields:
        if (form[field] is None):
            flash('Terjadi kesalahan saat menambahkan data', 'danger')
            return redirect(url_for(f'{module}.create'))

    # save model
    model = MataKuliah(
        nama=form['nama'],
        flag=1
    )

    # commit
    db.session.add(model)
    db.session.commit()

    flash('Data telah ditambahkan', 'info')
    return redirect(url_for(f'{module}.index'))


def edit(id):
    title = "Edit Matkul"
    model = _fetchById(id)
    return render_template(template + 'edit.html', title=title, module=module, model=model)


def update(id):
    form = request.form
    form_keys = form.keys()
    model = _fetchById(id)

    if "nama" in form_keys:
        model.nama = form['nama']

    db.session.commit()
    flash('Data berhasil diubah', 'info')
    return redirect(url_for(f'{module}.index'))


def destroy(id):
    model = _fetchById(id)
    model.flag = 0
    db.session.commit()
    flash('Data berhasil diubah', 'info')
    return redirect(url_for(f'{module}.index'))
