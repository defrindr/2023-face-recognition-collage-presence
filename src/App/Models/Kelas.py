from hashlib import md5
from . import Base
from App.Core.database import db
from sqlalchemy import Column, String, JSON, Integer, Enum


class Kelas(db.Model):
    __tablename__ = 'kelas'
    id = Column(Integer, primary_key=True)
    fakultas = Column(String(255))
    prodi = Column(String(255))
    kelas = Column(String(255))
    flag = Column(Integer, default=1)
    pass


def _getListFakultas():
    return [
        "TEKNIK",
        "BAHASA",
        "MIPA"
    ]


def _getListProdi():
    return {
        "TEKNIK": [
            "TEKNIK INFORMATIKA",
            "TEKNIK MESIN",
        ],
        "BAHASA": [
            "BAHASA INDONESIA",
            "BAHASA INGGRIS",
        ],
        "MIPA": [
            "MATEMATIKA",
            "FISIKA",
            "KIMIA",
        ],
    }


def _getProdi(fakultas):
    return getListProdi()[fakultas]


def _fetchByCriteria(fakultas, prodi, kelas):
    return Kelas.query.filter(
        Kelas.fakultas == fakultas,
        Kelas.prodi == prodi,
        Kelas.kelas == kelas,
        Kelas.flag == 1
    ).first()


def _fetchById(id):
    return Kelas.query.filter(Kelas.id == id, Kelas.flag == 1).first()


def _baseQuery():
    return Kelas.query.filter(
        Kelas.flag == 1
    ).order_by(Kelas.id.desc())
