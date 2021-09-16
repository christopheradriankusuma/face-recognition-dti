import cv2
from matplotlib import pyplot as plt
camera = 0

def plt_show(image, title=""):
    if len(image.shape) == 3:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    plt.axis("off")
    plt.title(title)
    plt.close()

# video camera
class NyalaVideo(object):
    def __init__(self, index=camera):
        self.video = cv2.VideoCapture(index) #Raspberry Mode
        # self.video = cv2.VideoCapture(index, cv2.CAP_DSHOW) #Untuk pengembangan
        self.index = index
        print (self.video.isOpened())

    def __del__(self):
        self.video.release()

    def get_frame(self, in_grayscale=False):
        _, frame = self.video.read()
        if in_grayscale:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        return frame

def baca_qr(nyalain):
    #cv2.startWindowThread()

    #nyalain = cv2.VideoCapture(camera) #Raspberry Mode
    #nyalain = cv2.VideoCapture(camera, cv2.CAP_DSHOW) #Untuk Pengembangan
    #_, frame = nyalain.read()
    #nyalain.release()

    #nyalain = NyalaVideo(camera)

    cv2.namedWindow("Baca QR", cv2.WINDOW_AUTOSIZE)

    token = ""
    for i in range(200):
        frame = nyalain.get_frame()
        plt_show(frame, "Baca QR")
        cv2.imshow(f"Baca QR", frame)
        cv2.waitKey(50)
        det = cv2.QRCodeDetector()
        val, pts, st_code = det.detectAndDecode(frame)
        token = val
        if token:
            break
    cv2.destroyAllWindows()
    del nyalain
    return token
