from code import compile_command
from textwrap import indent
import tkinter as tk
import os
from tkinter import messagebox
import tkinter.filedialog
from turtle import right
from cv2 import resize
from Cropper import crop
from PIL import Image, ImageTk
from tkinter import W, Frame, PhotoImage, ttk
import cv2 as cv

from ScannerImage import ScannerImage

class App(tk.Tk):
    def __init__(self):
        super().__init__()        
        self.images = list()
        self.image_index = 0
        self.img = None

        self.zoomin_level = 0
        self.zoomout_level = 0

        self.currentimg = None

        self.menu = tk.Menu(self)
        self.file = tk.Menu(self.menu,tearoff=0)
        self.middleframe = tk.Frame(self, highlightbackground="black", highlightthickness=2, relief=tk.SUNKEN)
        self.label = ttk.Label(self.middleframe,text='No Image' ,image = None)
        self.resizerframe = tk.Frame(self, highlightbackground="black", highlightthickness=2, relief=tk.SUNKEN)
        self.previousimage = ttk.Button(self.middleframe, text="Prev")
        self.nextimage = ttk.Button(self.middleframe, text="Next")
        self.resizedown = ttk.Button(self.resizerframe, text="Zoom Out")
        self.resizeup = ttk.Button(self.resizerframe, text="Zoom In")
        tk.Grid.rowconfigure(self, 0, weight=1)
        tk.Grid.columnconfigure(self, 0, weight=1)

        self.menu.add_cascade(label='File',menu=self.file)
        self.file.add_command(label="Open", command = self.selectmultiplefiles)
        self.file.add_command(label="Select Folder", command= self.choosefolder)
        self.file.add_command(label="Reset", command= self.clearimages)        

        self.middleframe.grid(column=0, row=0, sticky="EW")
        self.middleframe.columnconfigure(0, weight=1)

        self.label.grid(column=0,row=0, rowspan=2, sticky="W")
        self.previousimage.config(command=self.prevImage)
        self.previousimage.grid(column=1, row=0, sticky="SE")
        self.nextimage.config(command=self.nextImage)
        self.nextimage.grid(column=1,row=1, sticky="NE")
        self.resizerframe.columnconfigure(0, weight=1)
        self.resizerframe.columnconfigure(1, weight=1)
        self.resizerframe.grid(column=0, row=2, sticky="sew")
        self.resizedown.config(command=self.zoomout)
        self.resizedown.grid(column=0, row=0, sticky="S")
        self.resizeup.config(command=self.zoomin)
        self.resizeup.grid(column=1, row=0, sticky="S")

        self.bind('<Up>',self.zoominevent)
        self.bind('<Down>',self.zoomoutevent)
        self.bind('<Right>', self.nextImageEvent)
        self.bind('<Left>',self.prevImageEvent)
        self.config(menu=self.menu)

    def display_image(self):
        self.currentimg = self.images[self.image_index]
        if self.currentimg!=None:
            self.img = ImageTk.PhotoImage(image=self.currentimg)
            self.label.configure(image=self.img)
        else:
            print("Image not loaded")

    def selectmultiplefiles(self):
        filepaths = tkinter.filedialog.askopenfilenames(initialdir=os.curdir+"/images")
        self.openmultipleimages(filepaths)

    def openmultipleimages(self, filepaths):
        for filepath in filepaths:
            opened_image = Image.open(filepath)
            if(opened_image.width > 500 and opened_image.width > opened_image.height):
                ratio = 500/opened_image.width
                opened_image = opened_image.resize((500,int(opened_image.height*ratio)))

            elif(opened_image.height > 500 and opened_image.width < opened_image.height):
                ratio = 500/opened_image.width
                opened_image = opened_image.resize((500,int(opened_image.height*ratio)))
            self.images.append(opened_image)
            self.display_image()

    def choosefolder(self):
        folder = tkinter.filedialog.askdirectory(initialdir=os.curdir+"/images")
        self.openmultipleimages([folder+"/"+i for i in os.listdir(folder)])

    def clearimages(self):
        self.images = []
        self.img = None
        self.currentimg = None

    def zoomout(self):
        if self.currentimg!=None:
            self.zoomout_level+=1
            self.zoomin_level-=1
            image = self.images[self.image_index].resize((int(self.images[self.image_index].width*0.9**self.zoomout_level),int(self.images[self.image_index].height*0.9**self.zoomout_level)))
            self.img = ImageTk.PhotoImage(image=image)
            self.label.configure(image=self.img)
        else:
            messagebox.showwarning("No Image", "Add an image")
            print("Image not loaded")


    def zoomin(self):
        if self.currentimg!=None:
            self.zoomout_level-=1
            self.zoomin_level+=1
            image = self.images[self.image_index].resize((int(self.images[self.image_index].width*1.1**self.zoomin_level),int(self.images[self.image_index].height*1.1**self.zoomin_level)))
            self.img = ImageTk.PhotoImage(image=image)
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
    
root = App()
root.geometry("1280x720+200+0")
root.mainloop()
