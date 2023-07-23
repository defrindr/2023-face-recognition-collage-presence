from App.Models.KelasMahasiswa import KelasMahasiswa
from App.Models.User import Role, User
from App.Core.database import db


def _getListMahasiswaNotAssign():
    list_user = User.query.filter(
        User.role == Role.MAHASISWA,
        User.id.not_in(
            db.session.query(KelasMahasiswa.mahasiswa_id).subquery()
        )
    ).all()
    return list_user
