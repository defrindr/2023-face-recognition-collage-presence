from . import Base
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
    pass
