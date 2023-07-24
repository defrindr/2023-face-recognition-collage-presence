
from datetime import datetime
import os
from flask import jsonify
from sqlalchemy import or_
from App.Core.database import db
from App.Auth.auth_session import loggedInUser
from App.Models import Kelas as KelasModel, KelasMahasiswa, Presensi, User
from App.Models import Jadwal as JadwalModel
from App.Models import MataKuliah as MataKuliahModel
from App.Models.Jadwal import _baseQuery
from facerec import predict_face


def _getKelas(kelas):
    return KelasModel.query.filter(KelasModel.id == kelas, KelasModel.flag == 1).first()


def _indexService(kelas, page, per_page, search):
    title = f"Jadwal {kelas.prodi} {kelas.kelas}"
    headers = ['No', 'Hari', 'Mata Kuliah', 'Jam Mulai', 'Jam Selesai', 'Aksi']

    baseQuery = _baseQuery()

    if search != '':
        baseQuery = baseQuery.join(MataKuliahModel).filter(
            JadwalModel.kelas_id == kelas.id,
            MataKuliahModel.flag == 1,
            or_(
                JadwalModel.hari.like(f"%{search}%"),
                JadwalModel.jam_mulai.like(f"%{search}%"),
                JadwalModel.jam_selesai.like(f"%{search}%"),
                MataKuliahModel.nama.like(f"%{search}%"),
            )
        )
    else:
        baseQuery = baseQuery.join(MataKuliahModel).filter(
            JadwalModel.kelas_id == kelas.id,
            MataKuliahModel.flag == 1,
        )

    total_data = baseQuery.count()
    pagination = baseQuery.paginate(page=page, per_page=per_page)
    start_data = page * per_page - per_page
    len_items = len(pagination.items)

    return total_data, pagination, start_data, len_items, title, headers


def _presensiVideo(request):
    base_dir = "facerec/training/"
    temp_dir = f"{base_dir}/temp"
    temp_video_path = temp_dir+'/face_predict.mp4'

    # Check if 'temp' directory exists, if not, create one
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)

    # save video
    video = request.files['video']
    id = request.form['face_label']
    video.save(temp_video_path)

    c, id_user = predict_face(temp_video_path)
    current_user = loggedInUser()

    if int(id_user) != current_user.id:
        return jsonify({'message': 'Presensi gagal, terdeteksi sebagai orang lain!', 'confidence': c, 'label': id_user})

    if c < 70:
        return jsonify({'message': 'Gambar kurang jelas!', 'confidence': c, 'label': id_user})

    jadwal = JadwalModel.query.join(KelasModel, KelasMahasiswa, User).filter(
        User.id == current_user.id,
        JadwalModel.id == id
    ).first()

    if jadwal is None:
        return jsonify({'message': 'Presensi gagal, tidak dapat melakukan presensi!', 'confidence': c, 'label': id_user})

    # Get the current date and time
    current_datetime = datetime.now()

    # Format the date and time as 'Y-m-d H:i:s'
    formatted_date = current_datetime.strftime('%Y-%m-%d')
    formatted_time = current_datetime.strftime('%H:%M:%S')
    
    # check if already present
    presence_exist = Presensi.query.filter(Presensi.jadwal_id == id, Presensi.user_id == current_user.id, Presensi.tanggal == formatted_date).first()
    
    if presence_exist is not None:
        return jsonify({'message': 'Presensi gagal, sudah melakukan presensi sebelumnya!', 'confidence': c, 'label': id_user})
    
    # insert data
    presensi_record = Presensi(
        user_id=current_user.id,
        jadwal_id=id,
        kelas_id=jadwal.kelas_id,
        mata_kuliah_id=jadwal.mata_kuliah_id,
        tanggal=formatted_date,
        jam=formatted_time,
        photo="null"
    )

    db.session.add(presensi_record)
    db.session.commit()

    return jsonify({'message': 'Presensi berhasil!', 'confidence': c, 'label': id_user})
