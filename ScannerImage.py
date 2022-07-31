import cv2 as cv
import tkinter as tk
from PIL import Image, ImageTk
import math
from cv2 import getThreadNum
import numpy
import Cropper as cvUtils
import numpy as np
import copy


class ScannerImage():
    def __init__(self, filepath = "./assets/noimage.png"):
        self.pil_image = Image.open(filepath)
        self.tk_image = ImageTk.PhotoImage(image = self.pil_image)
        self.cv_image = cv.cvtColor(numpy.array(self.pil_image),cv.COLOR_RGB2BGR)

        self.outline_image, self.thresh_image = cvUtils.crop(self.cv_image)

        self.zoomin_level = 0
        self.zoomout_level = 0

        self.showing_thresh = False
        self.showing_outline = False

        if filepath=="./images/noimage.png":
            self.NO_IMAGE = False
        else:
            self.NO_IMAGE = True

        self.shown_image = ImageTk.PhotoImage(image = self.fit_image())
        
        self.update_dims()
        
        print(self.img_height)

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

    def update_dims(self):
        self.img_width = self.shown_image.width()
        self.img_height = self.shown_image.height()
        print(self.img_height)


    def zoomout(self):
        self.zoomout_level+=1
        self.zoomin_level-=1
        if(not self.showing_outline and not self.showing_thresh):
            self.shown_image = ImageTk.PhotoImage(self.pil_image.resize((int(self.pil_image.width*0.9**self.zoomout_level),
                                                                        int(self.pil_image.height*0.9**self.zoomout_level))))
        elif(self.showing_thresh):
            thresh_height = np.size(self.thresh_image, 0)
            thresh_width = np.size(self.thresh_image, 1)

            thresh = cv.resize(self.thresh_image,(int(self.pil_image.width*0.9**self.zoomout_level),
                                                  int(self.pil_image.height*0.9**self.zoomout_level)))
            thresh = cv.cvtColor(thresh, cv.COLOR_BGR2RGB)
            self.shown_image = ImageTk.PhotoImage(Image.fromarray(thresh))

        elif(self.showing_outline):
            outline_height = np.size(self.outline_image, 0)
            outline_width = np.size(self.outline_image, 1)
            
            outline = cv.resize(self.outline_image,(int(self.pil_image.width*0.9**self.zoomout_level),
                                                  int(self.pil_image.height*0.9**self.zoomout_level)))
            outline = cv.cvtColor(outline, cv.COLOR_BGR2RGB)
            self.shown_image = ImageTk.PhotoImage(Image.fromarray(outline))
        self.update_dims()

    def zoomin(self):
        self.zoomin_level+=1
        self.zoomout_level-=1
        print(self.zoomin_level)
        if(not self.showing_outline and not self.showing_thresh):
            self.shown_image = ImageTk.PhotoImage(self.pil_image.resize((int(self.pil_image.width*1.1**self.zoomin_level),
                                                                        int(self.pil_image.height*1.1**self.zoomin_level))))
        elif(self.showing_thresh):
            # thresh_height = np.size(self.thresh_image, 0)
            # thresh_width = np.size(self.thresh_image, 1)

            thresh = cv.resize(self.thresh_image,(int(self.pil_image.width*1.1**self.zoomin_level),
                                                  int(self.pil_image.height*1.1**self.zoomin_level)))
            thresh = cv.cvtColor(thresh, cv.COLOR_BGR2RGB)
            self.shown_image = ImageTk.PhotoImage(Image.fromarray(thresh))
        elif(self.showing_outline):
            # outline_height = np.size(self.outline_image, 0)
            # outline_width = np.size(self.outline_image, 1)
            
            outline = cv.resize(self.outline_image,(int(self.pil_image.width*1.1**self.zoomin_level),
                                                  int(self.pil_image.height*1.1**self.zoomin_level)))
            outline = cv.cvtColor(outline, cv.COLOR_BGR2RGB)
            self.shown_image = ImageTk.PhotoImage(Image.fromarray(outline))
        self.update_dims()

    def getThresh(self):
        thresh = cv.resize(self.thresh_image,(self.img_width, self.img_height))
        thresh = cv.cvtColor(thresh, cv.COLOR_BGR2RGB)
        self.showing_outline = False
        self.showing_thresh = True
        return ImageTk.PhotoImage(Image.fromarray(thresh))

    def getOutline(self):
        outline = cv.resize(self.outline_image,(self.img_width, self.img_height))
        outline = cv.cvtColor(outline, cv.COLOR_BGR2RGB)
        self.showing_thresh = False
        self.showing_outline = True
        return ImageTk.PhotoImage(Image.fromarray(outline)) 

    def noFilters(self):
        self.showing_outline = False
        self.showing_thresh = False

        