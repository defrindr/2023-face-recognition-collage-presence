from hashlib import md5
from .Base import Base
from App.Core.database import db
from sqlalchemy import Column, String, JSON, Integer, Enum


class MataKuliah(db.Model):
    __tablename__ = 'mata_kuliah'

    id = Column(Integer, primary_key=True)
    nama = Column(String(255), unique=True)
    flag = Column(Integer, default=1)

    jadwal = db.relationship('Jadwal', back_populates='mata_kuliah')
    pass


def _fetchByName(name):
    return MataKuliah.query.filter(MataKuliah.nama == name, MataKuliah.flag == 1).first()


def _fetchById(id):
    return MataKuliah.query.filter(MataKuliah.id == id, MataKuliah.flag == 1).first()


def _baseQuery():
    return MataKuliah.query.filter(
        MataKuliah.flag == 1
    ).order_by(MataKuliah.id)
