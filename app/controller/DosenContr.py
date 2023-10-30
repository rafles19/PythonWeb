from app.model.dosen import Dosen
from app.model.mahasiswa import Mahasiswa

from app import response, app, db
from flask import request, jsonify,abort
import math

def index():
    try:
        dosen = Dosen.query.all()
        data = formatArray(dosen)
        return response.success(data, "success")
    
    except Exception as e:
        print(e)

        #   Fungsi index():
        #   Ini adalah fungsi yang akan dijalankan ketika pengguna mengakses rute /dosen dengan metode HTTP GET.
        #   Fungsi ini berusaha untuk mengambil data semua dosen dari database dengan menggunakan Dosen.query.all().
        #   Data dosen yang diambil akan diformat menggunakan fungsi formatarray().
        #   Kemudian, data yang diformat dikirimkan sebagai respons dengan status "success" menggunakan modul response.

def formatArray(datas):
    array = []
    for i in datas:
        array.append(singleObject(i))
    
    return array

    #   Fungsi formatarray(datas):
    #   Fungsi ini digunakan untuk mengambil daftar objek dosen dan mengubahnya menjadi daftar objek JSON yang siap dikirimkan sebagai respons.
    #   Untuk setiap objek dosen, fungsi ini memanggil singleObject() untuk mengubahnya menjadi format JSON.

def singleObject(data):
    data = {
        'id': data.id,
        'nidn' : data.nidn,
        'nama' : data.nama,
        'phone' : data.phone,
        'alamat' : data.alamat
    }

    return data

    #   Fungsi singleObject(data)
    #   Fungsi ini mengambil objek dosen tunggal dan mengubahnya menjadi objek JSON dengan properti 
    #   seperti 'id', 'nidn', 'nama', 'phone', dan 'alamat'.

def detail(id):
    try:
        dosen = Dosen.query.filter_by(id=id).first()
        mahasiswa = Mahasiswa.query.filter((Mahasiswa.dosen_satu == id) | (Mahasiswa.dosen_dua == id))

        if not dosen:
            return response.badRequest([], 'Tidak ada data')
        
        datamahasiswa = formatMahasiswa(mahasiswa)

        data = singleDetailMahasiswa(dosen ,datamahasiswa)


        return response.success(data, "success")
    
    except Exception as e:
        print(e)
    
    #   Fungsi detail(id):
    #   Ini adalah fungsi yang akan dijalankan ketika pengguna mengakses rute /dosen/<id> dengan metode HTTP GET, di mana <id> adalah ID dosen yang ditentukan dalam URL.
    #   Fungsi ini berusaha untuk mengambil detail dosen dengan ID yang sesuai dari database.
    #   Selain itu, juga mencoba untuk mengambil daftar mahasiswa yang dibimbing oleh dosen tersebut.
    #   Jika dosen dengan ID yang diberikan tidak ditemukan, maka akan mengembalikan respons dengan status "badRequest" dan pesan 'Tidak ada data'.
    #   Jika dosen ditemukan, maka data dosen dan data mahasiswa akan digabungkan menjadi satu objek JSON dan dikirimkan sebagai respons dengan status "success" menggunakan modul response.


def singleMahasiswa(mahasiswa):
    data = {
        'id': mahasiswa.id,
        'nim': mahasiswa.nim,
        'nama': mahasiswa.nama,
        'phone': mahasiswa.phone
    }

    return data

def singleDetailMahasiswa(dosen, mahasiswa):
    data = {
        'id' : dosen.id,
        'nidn' : dosen.nidn,
        'nama' : dosen.nama,
        'phone' : dosen.phone,
        'mahasiswa' : mahasiswa
    }

    return data


def formatMahasiswa(data):
    array = []
    for i in data:
        array.append(singleMahasiswa(i))
    return array

def save():
    try:
        nidn = request.form.get('nidn')
        nama = request.form.get('nama')
        phone = request.form.get('phone')
        alamat = request.form.get('alamat')

        dosens = Dosen(nidn=nidn, nama=nama, phone=phone, alamat=alamat)
        db.session.add(dosens)
        db.session.commit()

        return response.success('', 'Sukses input data dosen')
    
    except Exception as e:
        print(e)


# Update Data

def ubah(id):
    try:
        nidn = request.form.get('nidn')
        nama = request.form.get('nama')
        phone = request.form.get('phone')
        alamat = request.form.get('alamat')

        input = [
            {
                'nidn' : nidn,
                'nama' : nama,
                'phone' : phone,
                'alamat' : alamat
            }
        ]

        dosen = Dosen.query.filter_by(id=id).first()

        dosen.nidn = nidn,
        dosen.nama = nama,
        dosen.phone = phone,
        dosen.alamat = alamat

        db.session.commit()
        
        return response.success(input, 'Sukses Mengubah Data')
    
    except Exception as e:
        print(e)

def hapus(id):
    try:
        dosen = Dosen.query.filter_by(id=id).first()

        if not dosen:
            return response.badRequest([], "Tidak ada data dosen")
        
        db.session.delete(dosen)
        db.session.commit()

        return response.success('', 'Berhasil Menghapus Data')
    except Exception as e:
        print(e)



def get_paginated_list(clss, url, start, limit):
    # Ambil query dari tabel dosen (class yang akan dibuat paginasi)
    results = clss.query.all()
    # Ubah format hasil query agar terserialisasi (dalam bentuk array)
    data = formatArray(results)
    # Hitung jumlah data dalam array
    count = len(data)

    obj = {}

    if (count < start):
        # Jika 'start' melebihi jumlah data yang ada
        obj['success'] = False
        obj['message'] = "Halaman yang dipilih (start) melewati batas total data!"
        return obj
    else:
        # Buat respons berhasil
        obj['success'] = True
        obj['start_page'] = start
        obj['per_page'] = limit
        obj['total_data'] = count
        # Menghitung total halaman (dibulatkan ke atas)
        obj['total_page'] = math.ceil(count / limit)
        # Membuat URL
        # Membuat URL halaman sebelumnya
        if start == 1:
            obj['previous'] = ''
        else:
            # Menentukan nilai 'start' yang akan digunakan di halaman sebelumnya
            start_copy = max(1, start - limit)
            # Menentukan nilai 'limit' untuk halaman sebelumnya
            limit_copy = start - 1
            # Membuat URL halaman sebelumnya
            obj['previous'] = url + '?start=%d&limit=%d' % (start_copy, limit_copy)
        # Membuat URL halaman berikutnya
        if start + limit > count:
            obj['next'] = ''
        else:
            # Menentukan nilai 'start' yang akan digunakan di halaman berikutnya
            start_copy = start + limit
            # Membuat URL halaman berikutnya
            obj['next'] = url + '?start=%d&limit=%d' % (start_copy, limit)
        # Menghasilkan hasil sesuai dengan batasan halaman
        # Mengambil subset dari data yang sesuai dengan halaman saat ini
        obj['results'] = data[(start - 1):(start - 1 + limit)]
        return obj


#buat fungsi paginate
def paginate():
    #ambil parameter get 
    #sample http://127.0.0.1:5000/api/dosen/page?start=3&limit=4
    start = request.args.get('start')
    limit = request.args.get('limit')

    try:
        #default display first page
        if start == None or limit == None:
            return jsonify(get_paginated_list(
            Dosen, 
            'http://127.0.0.1:5000/api/dosen/page', 
            start=request.args.get('start',1), 
            limit=request.args.get('limit',5)
            ))
            #custom parameters
        else:
            return jsonify(get_paginated_list(
            Dosen, 
            'http://127.0.0.1:5000/api/dosen/page', 
            start=int(start), 
            limit=int(limit)
            ))

    except Exception as e:
        print(e)