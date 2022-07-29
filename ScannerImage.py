import cv2 as cv
import tkinter as tk
from PIL import Image, ImageTk
import math
import copy


class ScannerImage():
    def __init__(self, filepath = "./images/noimage.png"):
        self.pil_image = Image.open(filepath)
        self.tk_image = ImageTk.PhotoImage(image = self.pil_image)

        self.zoomin_level = 0
        self.zoomout_level = 0

        if filepath=="./images/noimage.png":
            self.NO_IMAGE = False
        else:
            self.NO_IMAGE = True

        self.shown_image = ImageTk.PhotoImage(image = self.fit_image())

    def fit_image(self) -> Image:
        '''
        Function to resize a loaded image to fit inside the window
        '''


        if(self.pil_image.width > 500 or self.pil_image.height > 500):
            if(self.pil_image.width > self.pil_image.height):
                ratio_w = 500/self.pil_image.width
                self.zoomout_level = round(math.log(ratio_w, 0.9))
                self.zoomin_level = -self.zoomout_level
                return self.pil_image.resize((int(self.pil_image.width*0.9**self.zoomout_level),
                                              int(self.pil_image.height*0.9**self.zoomout_level)))
            elif(self.pil_image.width < self.pil_image.height):
                ratio_h = 500/self.pil_image.height
                self.zoomout_level = round(math.log(ratio_h, 0.9))
                self.zoomin_level = -self.zoomout_level
                return self.pil_image.resize((int(self.pil_image.width*0.9**self.zoomout_level),
                                              int(self.pil_image.height*0.9**self.zoomout_level)))
        else:
            return copy.copy(self.pil_image)

    def zoomout(self):
        self.zoomout_level+=1
        self.zoomin_level-=1
        self.shown_image = ImageTk.PhotoImage(self.pil_image.resize((int(self.pil_image.width*0.9**self.zoomout_level),
                                                                     int(self.pil_image.height*0.9**self.zoomout_level))))

    def zoomin(self):
        self.zoomin_level+=1
        self.zoomout_level-=1
        self.shown_image = ImageTk.PhotoImage(self.pil_image.resize((int(self.pil_image.width*1.1**self.zoomin_level),
                                                                     int(self.pil_image.height*1.1**self.zoomin_level))))


        