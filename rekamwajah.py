from secret import SECRET_URL
import sys
import cv2
import os
from matplotlib import pyplot as plt
import pandas as pd
from bacaqr import baca_qr
from io import StringIO
import requests

#SetUp Port Kameranya
camera = 0

# new thread
cv2.startWindowThread()

def plt_show(image, title=""):
    if len(image.shape) == 3:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    plt.axis("off")
    plt.title(title)
    #plt.imshow(image, cmap="Greys_r")
    #plt.show()
    #plt.pause(1)
    plt.close()


nyalain = cv2.VideoCapture(camera) # Raspberry Mode
#nyalain = cv2.VideoCapture(camera, cv2.CAP_DSHOW) # Untuk Pengembangan
_, frame = nyalain.read()
nyalain.release()
#plt_show(frame)

# face detection
obyek = cv2.CascadeClassifier("xml/frontal_face.xml")

scale_factor = 1.2
min_neighbors = 5
min_size = (50, 50)
biggest_only = True
flags = cv2.CASCADE_FIND_BIGGEST_OBJECT |             cv2.CASCADE_DO_ROUGH_SEARCH if biggest_only else             cv2.CASCADE_SCALE_IMAGE

faces_coord = obyek.detectMultiScale(frame,
                                        scaleFactor=scale_factor,
                                        minNeighbors=min_neighbors,
                                        minSize=min_size,
                                        flags=flags)

# video camera
class NyalaVideo(object):
    def __init__(self, index=camera):
        self.video = cv2.VideoCapture(index) #Raspberry Mode
        #self.video = cv2.VideoCapture(index, cv2.CAP_DSHOW) #Untuk pengembangan
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
        flags = cv2.CASCADE_FIND_BIGGEST_OBJECT | cv2.CASCADE_DO_ROUGH_SEARCH if biggest_only else cv2.CASCADE_SCALE_IMAGE
        faces_coord = self.classifier.detectMultiScale(image,
                                                       scaleFactor=scale_factor,
                                                       minNeighbors=min_neighbors,
                                                       minSize=min_size,
                                                       flags=flags)
        return faces_coord

# live face detection
nyalain = NyalaVideo(camera) # front cam acer
obyek = KenaliWajah("xml/frontal_face.xml")

# crop images
def cut_faces(image, faces_coord):
    faces = []
    for (x, y, w, h) in faces_coord:
        w_rm = int(0.2 * w / 2)
        faces.append(image[y: y + h, x + w_rm: x + w - w_rm])

    return faces

# normalize images
def normalize_intensity(images):
    images_norm = []
    for image in images:
        is_color = len(image.shape) == 3
        if is_color:
            image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        images_norm.append(cv2.equalizeHist(image))
    return images_norm

# resize images
def resize(images, size=(100, 100)):
    images_norm = []
    for image in images:
        if image.shape < size:
            image_norm = cv2.resize(image, size,
                                    interpolation = cv2.INTER_AREA)
        else:
            image_norm = cv2.resize(image, size,
                                    interpolation = cv2.INTER_CUBIC)
        images_norm.append(image_norm)

    return images_norm

# normalize face
def normalize_faces(frame, faces_coord):
    faces = cut_faces(frame, faces_coord)
    faces = normalize_intensity(faces)
    faces = resize(faces)
    return faces

# rectangle line
def draw_rectangle(image, coords):
    for (x, y, w, h) in coords:
        w_rm = int(0.2 * w / 2)
        cv2.rectangle(image, (x + w_rm, y), (x + w - w_rm, y + h),
                              (200, 200, 0), 4)

# get and save image
token = baca_qr(nyalain)
print(token)
df = pd.read_csv(StringIO(requests.get(SECRET_URL).text), dtype={'NRP': object})
#print(df)
db_token = df[df['Token'] == token].values

if len(db_token) == 0:
    print('Token salah')
    sys.exit()

if not token:
    sys.exit()

id, nama, nrp, tkn = db_token[0]
folder = f"siswa/{nrp}"

if not os.path.exists(folder):
    cv2.namedWindow("Simpan Gambar", cv2.WINDOW_AUTOSIZE)
    os.mkdir(folder)
    counter = 1
    timer = 0
    while counter < 11:
        frame = nyalain.get_frame()
        faces_coord = obyek.detect(frame)
        if len(faces_coord) and timer % 700 == 50:
            faces = normalize_faces(frame, faces_coord)
            cv2.imwrite(folder + '/' + str(counter) + '.jpg', faces[0])
            plt_show(faces[0], "Gambar Tersimpan:" + str(counter))
            counter += 1
            os.system("/usr/bin/mpg123 1.mp3")
        draw_rectangle(frame, faces_coord)
        if counter < 11:
            cv2.putText(frame, f"{counter}/10", (5, frame.shape[0]-5), cv2.FONT_HERSHEY_DUPLEX, 1, (66, 55, 245), 1, cv2.LINE_AA)
        cv2.namedWindow(f"Simpan Gambar", cv2.WND_PROP_FULLSCREEN)
        cv2.setWindowProperty("Simpan Gambar",cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)
        cv2.imshow(f"Simpan Gambar", frame)
        cv2.waitKey(50)
        timer += 50
    cv2.destroyAllWindows()
else:
    print ("Pengguna sudah terdaftar")

del nyalain
