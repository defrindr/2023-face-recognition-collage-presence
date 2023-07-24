import enum
from hashlib import md5
from .Base import Base
from App.Core.database import db
from sqlalchemy import Column, Date, ForeignKey, String, JSON, Integer, Enum, Time


class Presensi(db.Model):
    __tablename__ = 'presensi'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    kelas_id = Column(Integer, ForeignKey('kelas.id'))
    jadwal_id = Column(Integer, ForeignKey('jadwal.id'))
    mata_kuliah_id = Column(Integer, ForeignKey('mata_kuliah.id'))
    tanggal = Column(Date)
    jam = Column(Time)
    photo = Column(String, default='-')

    # Define the relationships with other tables
    user = db.relationship('User', backref='presensi')
    kelas = db.relationship('Kelas', backref='presensi')
    jadwal = db.relationship('Jadwal', backref='presensi')
    mata_kuliah = db.relationship('MataKuliah', backref='presensi')
    pass


def _fetchById(id):
    return Presensi.query.filter(Presensi.id == id).first()


def _fetchLastUserPresence(id):
    return Presensi.query.filter(Presensi.user_id == id).order_by(Presensi.id.desc()).first()


def _baseQuery():
    return Presensi.query.filter().order_by(Presensi.id.desc())
