from datetime import datetime
from sqlalchemy import Time, and_, between, cast, or_
from App.Models import Kelas as KelasModel
from App.Models import Jadwal as JadwalModel
from App.Models import Presensi as PresensiModel
from App.Models import MataKuliah as MataKuliahModel
from App.Models.Jadwal import Hari, _fetchById
from App.Core.database import db
from App.Models.Jadwal import _baseQuery


def _getKelas(kelas):
    return KelasModel.query.filter(KelasModel.id == kelas, KelasModel.flag == 1).first()


def _indexService(kelas, page, per_page, search):
    title = f"Jadwal {kelas.prodi} {kelas.kelas}"
    headers = ['No', 'Hari', 'Mata Kuliah', 'Jam Mulai', 'Jam Selesai', 'Aksi']

    baseQuery = _baseQuery()

    if search != '':
        baseQuery = baseQuery.join(MataKuliahModel).filter(
            MataKuliahModel.flag == 1,
            JadwalModel.kelas_id == kelas.id,
            or_(
                JadwalModel.hari.like(f"%{search}%"),
                JadwalModel.jam_mulai.like(f"%{search}%"),
                JadwalModel.jam_selesai.like(f"%{search}%"),
                MataKuliahModel.nama.like(f"%{search}%"),
            )
        )
    else:
        baseQuery = baseQuery.join(MataKuliahModel).filter(
            MataKuliahModel.flag == 1,
            JadwalModel.kelas_id == kelas.id,
        )
        pass

    total_data = baseQuery.count()
    pagination = baseQuery.paginate(page=page, per_page=per_page)
    start_data = page * per_page - per_page
    len_items = len(pagination.items)

    return total_data, pagination, start_data, len_items, title, headers


def _createService(kelas_model):
    title = f"Tambah Jadwal {kelas_model.prodi} {kelas_model.kelas}"

    list_matakuliah = MataKuliahModel.query.filter(
        MataKuliahModel.flag == 1).all()
    list_hari = Hari

    return title, list_matakuliah, list_hari


def _storeService(form, kelas):
    required_fields = ['hari', 'mata_kuliah_id', 'jam_mulai', 'jam_selesai']
    for field in required_fields:
        if field not in form.keys():
            return {
                'success': False,
                'message': 'Terjadi kesalahan saat menambahkan data'
            }

    # check exist
    exist_model = JadwalModel.query\
        .filter(
            JadwalModel.kelas_id == kelas,
            JadwalModel.hari == form['hari'],
            JadwalModel.flag == 1,
            or_(
                between(
                    JadwalModel.jam_mulai,
                    form['jam_mulai'],
                    form['jam_selesai']
                ),
                between(
                    JadwalModel.jam_selesai,
                    form['jam_mulai'],
                    form['jam_selesai']
                ),
                JadwalModel.mata_kuliah_id == form['mata_kuliah_id'],
            ),
        ).first()

    if exist_model:
        return {
            'success': False,
            'message': 'Data telah dimasukkan sebelumnya'
        }

    # save model
    model = JadwalModel(
        hari=form['hari'],
        mata_kuliah_id=form['mata_kuliah_id'],
        jam_mulai=cast(form['jam_mulai'], Time),
        jam_selesai=cast(form['jam_selesai'], Time),
        kelas_id=kelas,
        flag=1
    )

    # commit
    db.session.add(model)
    db.session.commit()

    return {
        'success': True,
        'message': 'Data telah ditambahkan'
    }


def _deleteService(kelas, id):
    model = _fetchById(id)
    model.flag = 0
    db.session.commit()


def _english_to_indonesian_day(english_day):
    day_mapping = {
        "Monday": "SENIN",
        "Tuesday": "SELASA",
        "Wednesday": "RABU",
        "Thursday": "KAMIS",
        "Friday": "JUMAT",
        "Saturday": "SABTU",
        "Sunday": "MINGGU"
    }

    return day_mapping.get(english_day, "Invalid Day")


def strtotime(date_string):
    try:
        # Parse the date string into a datetime object
        date_obj = datetime.strptime(date_string, "%Y-%m-%d %H:%M:%S")

        # Get the Unix timestamp from the datetime object
        unix_timestamp = date_obj.timestamp()
        return int(unix_timestamp)

    except ValueError:
        print("Invalid date format")
        return None


def _bukaPresensi(kelas, id):
    model = _fetchById(id)
    # Get the current date and time
    current_datetime = datetime.now()

    # Get the day name from the current date
    current_day_name = current_datetime.strftime("%A")
    current_date = current_datetime.strftime("%Y-%m-%d")
    current_unixtime = current_datetime.timestamp()
    hari = _english_to_indonesian_day(current_day_name)

    if hari == "Invalid Day":
        return {
            'success': False,
            'message': 'Hari tidak Valid',
        }
    elif model.hari.value != hari:
        return {
            'success': False,
            'message': 'Presensi dapat dibuka, jika harinya sama',
        }
    elif strtotime(f"{current_date} {model.jam_mulai}") > current_unixtime:
        return {
            'success': False,
            'message': 'Presensi belum dapat dimulai',
        }
    elif strtotime(f"{current_date} {model.jam_selesai}") < current_unixtime:
        return {
            'success': False,
            'message': 'Presensi tidak dapat dimulai',
        }

    model.presensi_status = 1

    # generate absensi untuk semua siswa
    anggota_kelas = model.kelas.anggota_kelas
    
    # Get the current date and time
    current_datetime = datetime.now()

    # Format the date and time as 'Y-m-d H:i:s'
    formatted_date = current_datetime.strftime('%Y-%m-%d')
    for siswa in anggota_kelas:
        jadwal_presensi = PresensiModel.query.filter(
                PresensiModel.user_id==siswa.mahasiswa_id,
                PresensiModel.kelas_id==model.kelas_id,
                PresensiModel.jadwal_id==model.id,
                PresensiModel.mata_kuliah_id==model.mata_kuliah_id,
                PresensiModel.tanggal==formatted_date
        ).first()
        if(jadwal_presensi == None) :
            model_presensi = PresensiModel(
                user_id=siswa.mahasiswa_id,
                kelas_id=model.kelas_id,
                jadwal_id=model.id,
                mata_kuliah_id=model.mata_kuliah_id,
                tanggal=formatted_date,
                status=0
            )
            db.session.add(model_presensi)

    db.session.commit()
    return {
        'success': True,
        'message': 'Berhasil membuka presensi',
    }


def _tutupPresensi(kelas, id):
    model = _fetchById(id)
    # Get the current date and time
    current_datetime = datetime.now()

    # Get the day name from the current date
    current_day_name = current_datetime.strftime("%A")
    current_date = current_datetime.strftime("%Y-%m-%d")
    current_unixtime = current_datetime.timestamp()
    hari = _english_to_indonesian_day(current_day_name)

    if model.hari == "Invalid Day":
        return {
            'success': False,
            'message': 'Hari tidak Valid',
        }
    elif model.presensi_status != 1:
        return {
            'success': False,
            'message': 'Tidak dapat menutup presensi yang belum dibuka',
        }

    model.presensi_status = 0
    db.session.commit()
    return {
        'success': True,
        'message': 'Berhasil membuka presensi',
    }
