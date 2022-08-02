from code import compile_command
from pickle import NONE
from sys import maxsize
from textwrap import indent
import tkinter as tk
import os
from tkinter import BooleanVar, messagebox
import tkinter.filedialog
from turtle import right
from typing_extensions import IntVar
from cv2 import resize
from numpy import var
from sqlalchemy import false
from Cropper import crop
from PIL import Image, ImageTk
from tkinter import W, Frame, PhotoImage, ttk
import cv2 as cv
from SlideDisplay import SlideDisplay

from ScannerImage import ScannerImage

class App(tk.Tk):
    def __init__(self):
        super().__init__()        
        self.images = list()
        self.images: list[ScannerImage]
        self.image_index = 0

        self.zoomin_level = 0
        self.zoomout_level = 0

        self.NO_IMAGE = ScannerImage()

        self.currentimg = self.NO_IMAGE
        self.img = self.currentimg.shown_image

        self.thresh_button = BooleanVar()
        self.outline_button = BooleanVar()

        self.menu = tk.Menu(self)
        self.file = tk.Menu(self.menu,tearoff=0)
        self.right_click_menu = tk.Menu(self, tearoff=0)
        self.middleframe = tk.Frame(self, highlightbackground="black", highlightthickness=2, relief=tk.SUNKEN, height=500)
        self.label = ttk.Label(self.middleframe, image = self.currentimg.shown_image)
        self.slide_display = SlideDisplay(self.middleframe)
        self.resizerframe = tk.Frame(self, highlightbackground="black", highlightthickness=2, relief=tk.SUNKEN)
        self.previousimage = ttk.Button(self.middleframe, text="Prev")
        self.nextimage = ttk.Button(self.middleframe, text="Next")
        self.resizedown = ttk.Button(self.resizerframe, text="Zoom Out")
        self.resizeup = ttk.Button(self.resizerframe, text="Zoom In")

        self.menu.add_cascade(label='File',menu=self.file)
        self.file.add_command(label="Open", command = self.selectmultiplefiles)
        self.file.add_command(label="Select Folder", command= self.choosefolder)
        self.file.add_command(label="Reset", command= self.clearimages)        

        self.right_click_menu.add_checkbutton(label='Thresh', variable=self.thresh_button, command=self.show_thresh)
        self.right_click_menu.add_checkbutton(label='Outline', variable=self.outline_button, command=self.show_outline)

        self.middleframe.grid(column=0, row=0, sticky="EW")
        self.middleframe.columnconfigure(1, weight=1)
        self.middleframe.columnconfigure(0, weight=1)

        self.label.grid(column=1,row=0, rowspan=2, sticky="W")
        self.slide_display.grid(column=0,row=0, rowspan=2, sticky="NW", pady=20)
        self.previousimage.config(command=self.prevImage)
        self.previousimage.grid(column=2, row=0, sticky="SE")
        self.nextimage.config(command=self.nextImage)
        self.nextimage.grid(column=2,row=1, sticky="NE")

        self.resizerframe.columnconfigure(0, weight=1)
        self.resizerframe.columnconfigure(1, weight=1)
        self.resizerframe.grid(column=0, row=1, sticky="sew")
        self.resizedown.config(command=self.zoomout)
        self.resizedown.grid(column=0, row=0, sticky="S")
        self.resizeup.config(command=self.zoomin)
        self.resizeup.grid(column=1, row=0, sticky="S")

        self.rowconfigure(0, weight=1, minsize=591)
        self.columnconfigure(0, weight=1, minsize=500)

        self.bind('<Up>',self.zoominevent)
        self.bind('<Down>',self.zoomoutevent)
        self.bind('<Right>', self.nextImageEvent)
        self.bind('<Left>',self.prevImageEvent)
        self.bind('<Button-3>', self.right_click_event)
        self.bind('<Button-1>', self.left_click_event)
        self.bind("<MouseWheel>", self.scroll_slide)
        self.config(menu=self.menu)

    def display_image(self):
        self.currentimg = self.images[self.image_index]
        if self.currentimg!=None:
            self.img = self.currentimg.shown_image
            self.label.configure(image=self.img)
        else:
            print("Image not loaded")

    def selectmultiplefiles(self):
        filepaths = tkinter.filedialog.askopenfilenames(initialdir=os.curdir+"/images")
        self.openmultipleimages(filepaths)

    def openmultipleimages(self, filepaths):
        for filepath in filepaths:
            opened_image = ScannerImage(filepath=filepath)
            self.images.append(opened_image)
            self.slide_display.add_image_and_label(opened_image)
        self.display_image()

    def choosefolder(self):
        folder = tkinter.filedialog.askdirectory(initialdir=os.curdir+"/images")
        self.openmultipleimages([folder+"/"+i for i in os.listdir(folder)])

    def clearimages(self):
        self.images = []
        self.image_index = 0
        self.currentimg = self.NO_IMAGE
        self.img = self.currentimg.shown_image
        self.label.config(image=self.img)

    def show_thresh(self):
        if(self.currentimg==self.NO_IMAGE):
            self.thresh_button.set(False)
            return None
        self.outline_button.set(False)
        if(self.thresh_button.get()):
            self.img = self.currentimg.getThresh()
            self.label.config(image=self.img)
            self.currentimg.showing_thresh = True
            self.currentimg.showing_outline = False
        else:
            self.currentimg.getNormal()
            self.label.config(image = self.currentimg.shown_image)
            self.currentimg.noFilters()

    def show_outline(self):
        if(self.currentimg==self.NO_IMAGE):
            self.outline_button.set(False)
            return None
        self.thresh_button.set(False)
        if(self.outline_button.get()):
            self.img = self.currentimg.getOutline()
            self.label.config(image=self.img)
            self.currentimg.showing_outline = True
            self.currentimg.showing_thresh = False
        else:
            self.currentimg.getNormal()
            self.label.config(image = self.currentimg.shown_image)
            self.currentimg.noFilters()


    def zoomout(self):
        if self.currentimg!=self.NO_IMAGE:
            self.currentimg.zoomout()
            self.img = self.currentimg.shown_image
            self.label.configure(image=self.img)
        else:
            messagebox.showwarning("No Image", "Add an image")
            print("Image not loaded")

    def zoomin(self):
        if self.currentimg!=self.NO_IMAGE:
            print(self.middleframe.winfo_height())
            self.currentimg.zoomin()
            self.img = self.currentimg.shown_image
            self.label.configure(image=self.img)
        else:
            messagebox.showwarning("No Image", "Add an image")
            print("Image not loaded")

    def zoominevent(self, event):
        self.zoomin()

    def zoomoutevent(self, event):
        self.zoomout()

    def nextImage(self):
        self.image_index+=1
        if self.image_index==len(self.images):
            self.image_index = 0
        self.zoomin_level = 0
        self.zoomout_level = 0
        self.display_image()

    def prevImage(self):
        self.image_index-=1
        if self.image_index<0:
            self.image_index = len(self.images)-1
        self.zoomin_level = 0
        self.zoomout_level = 0
        self.display_image()

    def nextImageEvent(self,event):
        self.nextImage()

    def prevImageEvent(self,event):
        self.prevImage()

    def right_click_event(self, event: tk.Event):
        try:
            self.right_click_menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.right_click_menu.grab_release()
    
    def left_click_event(self, event: tk.Event):
        widget: tk.Widget = event.widget
        if(widget.winfo_parent() == self.slide_display.winfo_parent() + "." + self.slide_display.winfo_name()):
            widget: tk.Label
            widget.configure(bd=5, relief="sunken")

    def scroll_slide(self, event: tk.Event):
        if(event.x_root > self.slide_display.winfo_rootx() and 
                event.x_root < (self.slide_display.winfo_rootx() + self.slide_display.winfo_width()) and 
                event.y_root > self.slide_display.winfo_rooty() and 
                event.y_root < (self.slide_display.winfo_rooty() + self.slide_display.winfo_height())):
            self.slide_display.scroll(event.delta)
 
root = App()
root.geometry("1280x720+200+0")
root.mainloop()
