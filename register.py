import pandas as pd
import cv2
import random
import string
import sys
import csv
import qrcode

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

nama = sys.argv[1].strip()
nrp = sys.argv[2].strip()

temp = random.sample(all, length)
password = "".join(temp)

while password in token:
    temp = random.sample(all, length)
    password = "".join(temp)

qr = qrcode.make(password)

file = open("database.csv")
reader = csv.reader(file)
id = len(list(reader))

with open(r'database.csv', 'a', newline='') as f:
    fields=[id, nama, nrp, password]
    writer = csv.writer(f)
    writer.writerow(fields)
