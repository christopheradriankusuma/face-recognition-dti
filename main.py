import eel
import os
import sys

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

loc = resource_path('tampilan')
eel.init(loc)

@eel.expose
def rekamwajah():
    print("Lakukan Absensi")
    os.system('python rekamwajah.py') #Ganti sesuai versi python

@eel.expose
def catatKehadiran():
    print("Record Face ID Pengguna")
    os.system('python catatpengunjung.py') #Ganti sesuai versi python

@eel.expose
def register(nama,nrp):
    print("Register Pengguna")
    print("Nama: {} | NRP: {}".format(nama,nrp))
    os.system('python register.py {} {}'.format(nama,nrp))

eel.start('index.html', size=(1000, 600), mode='edge')
