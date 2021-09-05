import random
import string
import sys
import csv
import os

length = 6
upper = string.ascii_uppercase
num = string.digits
all = upper + num
temp = random.sample(all,length)
password = "".join(temp)
nama = sys.argv[1]
nrp = sys.argv[2]


if not os.path.exists('database.csv'):
    fields=['ID','Nama','NRP','Token']
    with open(r'database.csv', 'a',newline='') as f:
        writer = csv.writer(f)
        writer.writerow(fields)

file = open("database.csv")
reader = csv.reader(file)
id = len(list(reader))

with open(r'database.csv', 'a', newline='') as f:
    fields=[id, nama, nrp, password]
    writer = csv.writer(f)
    writer.writerow(fields)

