from secret import SECRET_URL
import cv2
import numpy as np
import os
import pandas as pd
from matplotlib import pyplot as plt
import time
import datetime
from csv import writer
import requests
from io import StringIO

camera = 0 #SetUp Port Kameranya

# images properties
def plt_show(image, title=""):
    if len(image.shape) == 3:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    plt.axis("off")
    plt.title(title)
    plt.imshow(image, cmap="Greys_r")
    #plt.show()
    plt.pause(2)
    plt.close()

# video camera
class NyalaVideo(object):
    def __init__(self, index=camera):
        self.video = cv2.VideoCapture(index) #Raspberry Mode
        #self.video = cv2.VideoCapture(index, cv2.CAP_DSHOW) #Untuk Pengembangan
        self.index = index
        print (self.video.isOpened())

    def __del__(self):
        self.video.release()

    def get_frame(self, in_grayscale=False):
        _, frame = self.video.read()
        if in_grayscale:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        return frame

# face detection
class KenaliWajah(object):
    def __init__(self, xml_path):
        self.classifier = cv2.CascadeClassifier(xml_path)

    def detect(self, image, biggest_only=True):
        scale_factor = 1.2
        min_neighbors = 5
        min_size = (75, 75)
        biggest_only = True
        flags = cv2.CASCADE_FIND_BIGGEST_OBJECT |                     cv2.CASCADE_DO_ROUGH_SEARCH if biggest_only else                     cv2.CASCADE_SCALE_IMAGE
        rekamWajah = self.classifier.detectMultiScale(image,
                                                       scaleFactor=scale_factor,
                                                       minNeighbors=min_neighbors,
                                                       minSize=min_size,
                                                       flags=flags)
        return rekamWajah

# crop images
def potongWajah(image, rekamWajah):
    faces = []
    for (x, y, w, h) in rekamWajah:
        w_rm = int(0.3 * w / 2)
        faces.append(image[y: y + h, x + w_rm: x + w - w_rm])

    return faces

# normalize images
def normalize_intensity(images):
    images_norm = []
    for image in images:
        is_color = len(image.shape) == 3
        if is_color:
            image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        images_norm.append(cv2.equalizeHist(image)) #Menyesuaikan kontrass menggunakan histogram citra
    return images_norm

# resize images
def resize(images, size=(100, 100)):
    images_norm = []
    for image in images:
        if image.shape < size:
            image_norm = cv2.resize(image, size,
                                    interpolation=cv2.INTER_AREA)
        else:
            image_norm = cv2.resize(image, size,
                                    interpolation=cv2.INTER_CUBIC)
        images_norm.append(image_norm)

    return images_norm

# normalize faces
def normalize_faces(frame, rekamWajah):
    faces = potongWajah(frame, rekamWajah)
    faces = normalize_intensity(faces)
    faces = resize(faces)
    return faces

# rectangle line
def draw_rectangle(image, coords):
    for (x, y, w, h) in coords:
        w_rm = int(0.2 * w / 2)
        cv2.rectangle(image, (x + w_rm, y), (x + w - w_rm, y + h),
                              (102, 255, 0), 1)

# dapatkan gambar dari kumpulan data
def collect_dataset():
    images = []
    labels = []
    labels_dic = {}
    members = [person for person in os.listdir("siswa/")]
    for i, person in enumerate(members):   # loop over
        labels_dic[i] = person
        for image in os.listdir("siswa/" + person):
            images.append(cv2.imread("siswa/" + person + '/' + image,
                                     0))
            labels.append(i)
    return (images, np.array(labels), labels_dic)

ts = time.time()
date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')

images, labels, labels_dic = collect_dataset()

lbphAlgo = cv2.face.LBPHFaceRecognizer_create()
lbphAlgo.train(images, labels)
print ("Models Trained Berhasil")

# cascade face and mask
detector = KenaliWajah("xml/frontal_face.xml")

# 0 usb webcam additional
nyalain = NyalaVideo(camera)

def inputData(list_of_elem):
    with open("absen.csv", 'a+', newline='') as write_obj:
        csv_writer = writer(write_obj)
        csv_writer.writerow(list_of_elem)

label2 = ""

detecting = True
timer = 0
while detecting:
    objek = nyalain.get_frame()
    rekamWajah = detector.detect(objek, False) #deteksi lebih dari satu wajah
    if timer == 0:
        df = pd.read_csv(StringIO(requests.get("https://absensi-dti.herokuapp.com/hayo-ngapain-kesini-dti-9987b6e63716f1c918d5ed38fb7b3bd7").text), dtype={'NRP': object})
    timer = (timer + 1) % 1000
    #Cek Face Recognition
    if len(rekamWajah):
        faces = normalize_faces(objek, rekamWajah)
        for i, face in enumerate(faces):
            collector = cv2.face.StandardCollector_create()
            lbphAlgo.predict_collect(face, collector)
            conf = collector.getMinDist()
            pred = collector.getMinLabel()
            threshold = 76 # eigen, fisher, lbph [mean 3375,1175,65] [high lbph 76]
            try:
                nama = df[df['NRP'] == labels_dic[pred]]['Nama'].values[0]
            except:
                continue
            print ("Nama: " + nama + "\nSkala Prediksi: " + str(round(conf)))
            if conf < threshold:
                cv2.putText(objek, nama,
                            (rekamWajah[i][0], rekamWajah[i][1] - 20),
                            cv2.FONT_HERSHEY_DUPLEX, 1.0, (102, 255, 0), 1)
                # Buat file baru dan Input data ke CSV file
                input = [nama,labels_dic[pred],date,timeStamp]
                Hour,Minute,Second=timeStamp.split(":")
                if(label2 != labels_dic[pred]):
                    inputData(input)
                label2 = labels_dic[pred]
                #plt_show(objek, nama)
            else:
                cv2.putText(objek, "Tidak Dikenali",
                    (rekamWajah[i][0], rekamWajah[i][1] - 10),
                    cv2.FONT_HERSHEY_DUPLEX, 1.0, (66, 55, 245), 1)
        draw_rectangle(objek, rekamWajah)
    cv2.putText(objek, "ESC to exit", (5, objek.shape[0] - 5),
    cv2.FONT_HERSHEY_DUPLEX, 1, (255, 255, 255), 1, cv2.LINE_AA)
    # Full screen mode
    cv2.namedWindow("Sistem Absensi Face Recognitions", cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty("Sistem Absensi Face Recognitions",cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)
    cv2.imshow("Sistem Absensi Face Recognitions", objek)
    if cv2.waitKey(33) & 0xFF == 27:
        cv2.destroyAllWindows()
        break

del nyalain
