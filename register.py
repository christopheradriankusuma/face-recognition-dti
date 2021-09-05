import random
import string
import sys
import csv
import pandas as pd

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

file = open("database.csv")
reader = csv.reader(file)
id = len(list(reader))

with open(r'database.csv', 'a', newline='') as f:
    fields=[id, nama, nrp, password]
    writer = csv.writer(f)
    writer.writerow(fields)
