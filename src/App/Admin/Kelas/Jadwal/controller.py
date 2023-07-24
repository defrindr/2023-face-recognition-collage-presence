from flask import render_template, request, url_for, flash, redirect, abort
from .service import _bukaPresensi, _createService, _deleteService, _getKelas, _indexService, _storeService, _tutupPresensi


module = "admin.kelas.jadwal"
template = 'Admin/Kelas/Jadwal/'


def index(kelas):
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
    )


def create(kelas):
    kelas_model = _getKelas(kelas)
    if kelas_model is None:
        return abort(404)

    title, list_matakuliah, list_hari = _createService(kelas_model)

    return render_template(
        template + 'create.html',
        title=title,
        module=module,
        kelas=kelas,
        list_matakuliah=list_matakuliah,
        list_hari=list_hari,
    )


def store(kelas):
    response = _storeService(request.form, kelas)

    if response['success'] == True:
        flash(response['message'], 'info')
        return redirect(url_for(f'{module}.index', kelas=kelas))
    else:
        flash(response['message'], 'danger')
        return redirect(url_for(f'{module}.create', kelas=kelas))


def destroy(kelas, id):
    kelas_model = _getKelas(kelas)
    _deleteService(kelas_model, id)

    flash('Data berhasil dihapus', 'info')
    return redirect(url_for(f'{module}.index', kelas=kelas))


def bukaPresensi(kelas, id):
    kelas_model = _getKelas(kelas)
    response = _bukaPresensi(kelas_model, id)

    flash(response['message'], 'info' if response['success'] else 'danger')
    return redirect(url_for(f'{module}.index', kelas=kelas))


def tutupPresensi(kelas, id):
    kelas_model = _getKelas(kelas)
    response = _tutupPresensi(kelas_model, id)

    flash(response['message'], 'info' if response['success'] else 'danger')
    return redirect(url_for(f'{module}.index', kelas=kelas))
