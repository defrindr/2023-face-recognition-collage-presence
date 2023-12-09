import io
import os
from tempfile import TemporaryDirectory
import cv2
from flask import jsonify, render_template, request, url_for, flash, redirect
from sqlalchemy import or_
import calendar
from App.Models.Jadwal import _AnggotaKelas
from datetime import date

module = "admin.report"
template = 'Admin/Report/'


def index(id):
    title = "Laporan Absensi"
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    search = request.args.get('search', '', type=str)
    month = request.args.get('month', default = date.today().month, type = int)
    year = request.args.get('year', default = date.today().year, type = int)

    currentYear = date.today().year

    month_range = calendar.monthrange(year, month)
    jumlah_hari_dalam_1bulan = month_range[1]
    tanggal = []
    baseQuery = _AnggotaKelas(id)

    if search != '':
        baseQuery = baseQuery.filter(
            or_(
                User.username.like(f"%{search}%"),
                User.name.like(f"%{search}%")
            )
        )
        pass

    print(baseQuery.all())
    total_data = baseQuery.count()
    pagination = baseQuery.paginate(page=page, per_page=per_page)
    print(pagination.items)
    start_data = page * per_page - per_page
    len_items = len(pagination.items)

    return render_template(
        template + 'index.html', 
        id=id,
        pagination=pagination, 
        len_items=len_items, 
        title=title, 
        module=module, 
        start_data=start_data, 
        per_page=per_page, 
        total_data=total_data, 
        search=search, 
        month=month, 
        year=year, 
        currentYear=currentYear,
        jumlah_hari_dalam_1bulan = jumlah_hari_dalam_1bulan
    )
