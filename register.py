import pandas as pd
import cv2
import random
import string
import sys
import csv
import qrcode
from datetime import datetime
import matplotlib.pyplot as plt

from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw 


def read(img):
    img = cv2.imread(img)
    det = cv2.QRCodeDetector()
    val, pts, st_code = det.detectAndDecode(img)
    print(val)

def create(data):
    return qrcode.make(data)

df = pd.read_csv('database.csv')
token = df['Token'].values

length = 6
upper = string.ascii_uppercase
num = string.digits
all = upper + num

# python.py das asda sda sdas dsa 13123123789

nama = sys.argv[1:-1]
nama_fix = ' '.join(nama)
nrp = sys.argv[-1]

temp = random.sample(all, length)
password = "".join(temp)

while password in token:
    temp = random.sample(all, length)
    password = "".join(temp)

qr = qrcode.make(password)

file = open("database.csv")
reader = csv.reader(file)
id = len(list(reader))

# tanggal_sekarang = datetime.today().strftime('%Y-%m-%d_%H-%M-%S')

lokasi_file = "tampilan/dist/images/qrcode/{}.png".format(nrp)

qr.save(lokasi_file)

## ADD TEXT TO IMAGE
image = Image.open(lokasi_file)
ukuran = image.size
draw = ImageDraw.Draw(image)

# font = ImageFont.load_default()
font = ImageFont.truetype("arial.ttf", 24)

# draw.text((x, y),"Sample Text",(r,g,b))
draw.text(((ukuran[0]//2)-32, (ukuran[1]*8.69)//10),password,fill=0,font=font)

# image.show()
image.save(lokasi_file)

with open(r'database.csv', 'a', newline='') as f:
    fields=[id, nama_fix, nrp, password]
    writer = csv.writer(f)
    writer.writerow(fields)
