from hashlib import md5
from .Base import Base
from .User import User
from App.Core.database import db
from sqlalchemy import Column, String, JSON, Integer, Enum, ForeignKey


class KelasMahasiswa(db.Model):
    __tablename__ = 'kelas_mhs'

    id = Column(Integer, primary_key=True)
    kelas_id = Column(Integer, ForeignKey('kelas.id'))
    mahasiswa_id = Column(Integer, ForeignKey('users.id'))
    
    # Many-to-one relationship with Kelas
    kelas = db.relationship('Kelas', back_populates='anggota_kelas')

    # Many-to-one relationship with User
    user = db.relationship('User', back_populates='anggota_kelas')

    pass


def _fetchById(id):
    return KelasMahasiswa.query.filter(KelasMahasiswa.id == id).first()


def _fetchByKelas(id):
    return KelasMahasiswa.query.filter(KelasMahasiswa.kelas_id == id).all()


def _fetchByMahasiswa(id):
    return KelasMahasiswa.query.filter(KelasMahasiswa.mahasiswa_id == id).all()


def _baseQuery():
    return KelasMahasiswa.query.join(User).filter(User.flag == 1).order_by(KelasMahasiswa.id.desc())