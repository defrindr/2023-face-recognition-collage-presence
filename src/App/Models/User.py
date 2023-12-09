from hashlib import md5

from .Base import Base
from App.Core.database import db
from sqlalchemy import Column, String, JSON, Integer, Enum
import enum
import os
from App.Models.Presensi import Presensi
from glob import glob
from flask import current_app as app

class Role(enum.Enum):
    ADMIN = "ADMIN"
    MAHASISWA = "MAHASISWA"
    pass


class User(db.Model):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(255), unique=True)
    password = Column(String(255))
    role = Column(Enum(Role))
    name = Column(String(255))
    photo = Column(String(255))
    flag = Column(Integer, default=1)

    anggota_kelas = db.relationship('KelasMahasiswa', back_populates='user')

    def path(self):
        base_dir = "facerec/training/"
        face_dir = f"{base_dir}/faces"
        face_label = self.id
        path_training = f"{face_dir}/{face_label}/"
        return path_training

    def hasTraining(self):
        return os.path.exists(self.path())

    def _checkAbsensiHariIni(self, tanggal, bulan, tahun, jadwal_id):
        adaJadwal = db.session.query(Presensi).filter(
            Presensi.tanggal == f"{tahun}-{bulan}-{tanggal}",
            Presensi.user_id == self.id,
            Presensi.jadwal_id == jadwal_id
        ).first()

        if adaJadwal is None: 
            return ""
        elif adaJadwal.status == 1:
            return "✓"
        else:
            return "x"

    def alreadyTraining(self):
        if self.hasTraining() == True:
            return "Sudah"
        else:
            return "Belum"

    def getPhotoProfile(self):
        path = app.root_path + "/static/profiles/" + self.username + ".png"

        if os.path.exists(path):
            return "/Static/profiles/" + self.username + ".png"
        else:
            return ""



    pass

def _hashPassword(plaintext):
    return md5(str(plaintext).encode()).hexdigest()

def _fetchByUsername(username):
    return User.query.filter(User.username == username, User.flag == 1).first()


def _fetchById(id):
    return User.query.filter(User.id == id, User.flag == 1).first()

def _baseQueryAdmin():
    return User.query.filter(
        User.role == Role.ADMIN,
        User.flag == 1
    ).order_by(User.username)

def _baseQuery():
    return User.query.filter(
        User.role == Role.MAHASISWA,
        User.flag == 1
    ).order_by(User.username)