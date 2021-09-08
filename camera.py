from PIL import Image
from PIL import ImageTk
import tkinter as tki
import threading
import datetime
import imutils
from imutils.video import VideoStream
import cv2
import os
import time

class PhotoApp:
    def __init__(self, vs, output_path='./'):
        self.vs = vs
        self.output_path = output_path
        self.frame = None
        self.thread = None
        self.stopEvent = None
		
        self.root = tki.Tk()
        self.panel = None

        # btn = tki.Button(self.root, text="Snapshot!", command=self.takeSnapshot)
        # btn.pack(side="bottom", fill="both", expand="yes", padx=10, pady=10)
        
        self.stopEvent = threading.Event()
        self.thread = threading.Thread(target=self.videoLoop, args=())
        self.thread.start()

        self.root.wm_title("Rekam wajah")
        self.root.wm_protocol("WM_DELETE_WINDOW", self.onClose)

    def videoLoop(self):
        try:
            while not self.stopEvent.is_set():
                self.frame = self.vs.read()
                self.frame = imutils.resize(self.frame, width=300)

                image = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
                image = Image.fromarray(image)
                image = ImageTk.PhotoImage(image)        
                
                if self.panel is None:
                    self.panel = tki.Label(image=image)
                    self.panel.image = image
                    self.panel.pack(side="left", padx=10, pady=10)
                else:
                    self.panel.configure(image=image)
                    self.panel.image = image
        except RuntimeError as e:
            print("[INFO] caught a RuntimeError")

    def takeSnapshot(self):
        ts = datetime.datetime.now()
        filename = "{}.jpg".format(ts.strftime("%Y-%m-%d_%H-%M-%S"))
        p = os.path.sep.join((self.outputPath, filename))

        cv2.imwrite(p, self.frame.copy())
        print("[INFO] saved {}".format(filename))

    def onClose(self):
        self.stopEvent.set()
        self.vs.stop()
        self.root.quit()

vs = VideoStream(usePiCamera=False).start()
time.sleep(2)

pa = PhotoApp(vs)
pa.root.mainloop()