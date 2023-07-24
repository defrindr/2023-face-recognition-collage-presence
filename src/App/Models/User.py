from hashlib import md5

from .Base import Base
from App.Core.database import db
from sqlalchemy import Column, String, JSON, Integer, Enum
import enum


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
    flag = Column(Integer, default=1)

    anggota_kelas = db.relationship('KelasMahasiswa', back_populates='user')
    pass

def _hashPassword(plaintext):
    return md5(str(plaintext).encode()).hexdigest()

def _fetchByUsername(username):
    return User.query.filter(User.username == username, User.flag == 1).first()


def _fetchById(id):
    return User.query.filter(User.id == id, User.flag == 1).first()


def _baseQuery():
    return User.query.filter(
        User.role == Role.MAHASISWA,
        User.flag == 1
    ).order_by(User.username)