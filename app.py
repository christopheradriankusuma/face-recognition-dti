from flask import Flask, request, render_template
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from flask.helpers import send_from_directory 
import pandas as pd
import re
import random
import string
import csv
import qrcode
import os

if not os.path.exists('database.csv'):
    fields = ['ID', 'Nama', 'No Induk', 'Tanggal lahir', 'Token']
    with open(r'database.csv', 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(fields)

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    nama = request.form.get('nama', '')
    nrp = request.form.get('nrp', '')

    nama_valid = re.findall(r'[a-zA-Z\' ]+', nama)
    nrp_valid = re.findall(r'\d+', nrp)

    if not nama_valid or not nrp_valid:
        error = "Pastikan nama/NRP yang anda masukkan benar"
        return render_template('index.html', error=error)

    if token:=tambah_user(nama, nrp):
        return render_template('index.html', img=f"images/{nrp}.png", token=token)
    else:
        return render_template('index.html', error="NRP telah terdaftar")

@app.route('/static/images/<string:nrp>', methods=['GET'])
def download(nrp):
    return send_from_directory('static/images/', nrp, as_attachment=True)

# @app.route('/secret', methods=['GET'])
# def db():
#     return send_from_directory('', 'database.csv', as_attachment=True)

def tambah_user(nama, nrp):
    df = pd.read_csv('database.csv', dtype={'NRP': object})

    tokens = df['Token'].values
    nrps = df['NRP'].values
    if nrp in nrps:
        return False

    length = 6
    upper = string.ascii_uppercase
    num = string.digits
    all = upper + num

    temp = random.sample(all, length)
    token = "".join(temp)

    while token in tokens:
        temp = random.sample(all, length)
        token = "".join(temp)

    lokasi_file = "static/images/{}.png".format(nrp)

    qr = qrcode.make(token)

    file = open("database.csv")
    reader = csv.reader(file)
    id = len(list(reader))
    qr.save(lokasi_file)

    image = Image.open(lokasi_file)
    ukuran = image.size
    draw = ImageDraw.Draw(image)

    font = ImageFont.truetype("static/fonts/arial.ttf", 24)
    draw.text(((ukuran[0]//2)-32, (ukuran[1]*8.69)//10), token, fill=0, font=font)

    image.save(lokasi_file)

    with open(r'database.csv', 'a', newline='') as f:
        fields = [id, nama, nrp, token]
        writer = csv.writer(f)
        writer.writerow(fields)

    return token