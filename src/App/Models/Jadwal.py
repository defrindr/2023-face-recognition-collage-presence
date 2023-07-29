import enum
from hashlib import md5

from App.Models import User
from App.Models.Presensi import Presensi
from .Base import Base
from App.Core.database import db
from sqlalchemy import Column, ForeignKey, String, JSON, Integer, Enum, Time
from datetime import date


class Hari(enum.Enum):
    SENIN = 'SENIN'
    SELASA = 'SELASA'
    RABU = 'RABU'
    KAMIS = 'KAMIS'
    JUMAT = 'JUMAT'
    SABTU = 'SABTU'
    MINGGU = 'MINGGU'
    pass


class Jadwal(db.Model):
    __tablename__ = 'jadwal'
    id = Column(Integer, primary_key=True)
    mata_kuliah_id = Column(Integer, ForeignKey('mata_kuliah.id'))
    kelas_id = Column(Integer, ForeignKey('kelas.id'))
    hari = Column(Enum(Hari))
    jam_mulai = Column(Time)
    jam_selesai = Column(Time)
    flag = Column(Integer, default=1)
    presensi_status = Column(Integer, default=0)

    kelas = db.relationship('Kelas', back_populates='jadwal')
    mata_kuliah = db.relationship('MataKuliah', back_populates='jadwal')

    def hasPresensiToday(self, user_id):
        today = date.today()
        attendance = Presensi.query.filter_by(
            tanggal=today, jadwal_id=self.id, user_id=user_id).first()
        return attendance is not None
    pass


def _fetchById(id):
    return Jadwal.query.filter(Jadwal.id == id, Jadwal.flag == 1).first()


def _baseQuery():
    return Jadwal.query.filter(
        Jadwal.flag == 1
    ).order_by(Jadwal.id.desc())
