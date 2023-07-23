from flask import render_template, request, url_for, flash, redirect, abort
from App.Admin import MataKuliah
from App.Core.database import db
from App.Models.Kelas import Kelas as KelasModel
from App.Models.KelasMahasiswa import _baseQuery, _fetchById, _fetchByKelas, _fetchByMahasiswa, KelasMahasiswa
from .service import _getListMahasiswaNotAssign


module = "admin.kelas.mahasiswa"
template = 'Kelas/Mahasiswa/'


def index(kelas):
    kelas_model = KelasModel.query.filter(KelasModel.id == kelas).first()
    if kelas_model is None:
        return abort(404)
    title = f"Anggota {kelas_model.prodi} {kelas_model.kelas}"
    headers = ['No', 'Anggota', 'Aksi']

    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    search = request.args.get('search', '', type=str)

    baseQuery = _baseQuery()

    if search != '':
        baseQuery = baseQuery.filter(
            KelasMahasiswa.nama.like(f"%{search}%")
        )
        pass

    total_data = baseQuery.count()
    pagination = baseQuery.paginate(page=page, per_page=per_page)
    start_data = page * per_page - per_page
    len_items = len(pagination.items)

    return render_template(template + 'index.html', pagination=pagination, len_items=len_items, headers=headers, title=title, module=module, start_data=start_data, per_page=per_page, total_data=total_data, search=search, kelas=kelas)


def create(kelas):
    kelas_model = KelasModel.query.filter(KelasModel.id == kelas).first()
    if kelas_model is None:
        return abort(404)
    title = f"Tambah Anggota {kelas_model.prodi} {kelas_model.kelas}"
    users = _getListMahasiswaNotAssign()
    return render_template(template + 'create.html', title=title, module=module, kelas=kelas, users=users)


def store(kelas):
    # validation
    required_fields = ['anggota']
    form = request.form
    for field in required_fields:
        if (form[field] is None):
            flash('Terjadi kesalahan saat menambahkan data', 'danger')
            return redirect(url_for(f'{module}.create', kelas=kelas))

    # save model
    model = KelasMahasiswa(
        kelas_id=kelas,
        mahasiswa_id=form['anggota'],
    )

    # commit
    db.session.add(model)
    db.session.commit()

    flash('Data telah ditambahkan', 'info')
    return redirect(url_for(f'{module}.index', kelas=kelas))

def destroy(kelas, id):
    model = _fetchById(id)
    db.session.delete(model)
    db.session.commit()
    flash('Data berhasil dihapus', 'info')
    return redirect(url_for(f'{module}.index', kelas=kelas))
