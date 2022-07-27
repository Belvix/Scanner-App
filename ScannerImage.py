import cv2 as cv
import tkinter as tk
from PIL import Image, ImageTk
import math
import copy


class ScannerImage():
    def __init__(self, filepath: str):
        self.pil_image = Image.open(filepath)
        self.tk_image = ImageTk.PhotoImage(image = self.pil_image)

        self.zoomin_level = 0
        self.zoomout_level = 0

        self.shown_image = self.fit_image()

    def fit_image(self) -> Image:
        '''
        Function to resize a loaded image to fit inside the window
        '''

        ratio_w = 500/self.pil_image.width
        ratio_h = 500/self.pil_image.height

        if(self.pil_image.width > 500 or self.pil_image.height > 500):
            if(self.pil_image.width > self.pil_image.height):
                math.log(ratio_w, 0.9)
                return self.pil_image.resize((500,int(self.pil_image.height*ratio_w)))
            elif(self.pil_image.width < self.pil_image.height):
                math.log(ratio_h, 0.9)
                return self.pil_image.resize((500,int(self.pil_image.height*ratio_h)))
        else:
            self.shown_image = copy.copy(self.pil_image)
        