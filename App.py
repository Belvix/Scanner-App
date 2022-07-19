from textwrap import indent
import tkinter as tk
import os
import tkinter.filedialog
from turtle import right

from cv2 import resize
from Cropper import crop
from PIL import Image, ImageTk
from tkinter import W, Frame, PhotoImage, ttk
import cv2 as cv

root = tk.Tk()

tk.Grid.rowconfigure(root, 0, weight=1)
tk.Grid.columnconfigure(root, 0, weight=1)

images = list()
image_index = 0
zoomin_level = 0
zoomout_level = 0


def display_image():
    global img, currentimg
    currentimg = images[image_index]
    if currentimg!=None:
        img = ImageTk.PhotoImage(image=currentimg)
        label.configure(image=img)
    else:
        print("Image not loaded")

def selectmultiplefiles():
    filepaths = tkinter.filedialog.askopenfilenames(initialdir=os.curdir+"/images")
    openmultipleimages(filepaths)


def openmultipleimages(filepaths):
    global currentimg, images

    for filepath in filepaths:
        opened_image = Image.open(filepath)
        if(opened_image.width > 500 and opened_image.width > opened_image.height):
            ratio = 500/opened_image.width
            opened_image = opened_image.resize((500,int(opened_image.height*ratio)))

        elif(opened_image.height > 500 and opened_image.width < opened_image.height):
            ratio = 500/opened_image.width
            opened_image = opened_image.resize((500,int(opened_image.height*ratio)))
        images.append(opened_image)
        display_image()
    print(images)

def zoomout():
    global img, zoomout_level, zoomin_level
    if currentimg!=None:
        zoomout_level+=1
        zoomin_level-=1
        image = images[image_index].resize((int(images[image_index].width*0.9**zoomout_level),int(images[image_index].height*0.9**zoomout_level)))
        img = ImageTk.PhotoImage(image=image)
        label.configure(image=img)
    else:
        print("Image not loaded")


def zoomin():
    global img, zoomout_level, zoomin_level
    if currentimg!=None:
        zoomout_level-=1
        zoomin_level+=1
        image = images[image_index].resize((int(currentimg.width*1.1**zoomin_level),int(currentimg.height*1.1**zoomin_level)))
        img = ImageTk.PhotoImage(image=image)
        label.configure(image=img)
    else:
        print("Image not loaded")

def zoominevent(event):
    zoomin()

def zoomoutevent(event):
    zoomout()

def nextImage():
    global image_index
    image_index+=1
    if image_index==len(images):
        image_index = 0
    display_image()

def prevImage():
    global image_index
    image_index-=1
    if image_index==0:
        image_index = len(images)
    display_image()

currentimg = None
menu = tk.Menu(root)
file = tk.Menu(menu,tearoff=0)
menu.add_cascade(label='File',menu=file)
file.add_command(label="Open", command = selectmultiplefiles)
menu.add_command(label="newfile", command=None)

middleframe = tk.Frame(root, highlightbackground="black", highlightthickness=2, relief=tk.SUNKEN)
middleframe.grid(column=0, row=0, sticky="EW")
middleframe.columnconfigure(0, weight=1)
label = ttk.Label(middleframe,text='No Image' ,image = None)
label.grid(column=0,row=0, rowspan=2, sticky="W")
previousimage = ttk.Button(middleframe, text="Prev", command=prevImage)
previousimage.grid(column=1, row=0, sticky="SE")
nextimage = ttk.Button(middleframe, text="Next", command=nextImage)
nextimage.grid(column=1,row=1, sticky="NE")

resizerframe = tk.Frame(root, highlightbackground="black", highlightthickness=2, relief=tk.SUNKEN)
resizerframe.columnconfigure(0, weight=1)
resizerframe.columnconfigure(1, weight=1)
resizerframe.grid(column=0, row=2, sticky="sew")
resizedown = ttk.Button(resizerframe, text="Zoom Out", command = lambda: zoomout())
resizedown.grid(column=0, row=0, sticky="S")
resizeup = ttk.Button(resizerframe, text="Zoom In", command = lambda: zoomin())
resizeup.grid(column=1, row=0, sticky="S")
root.bind('<Up>',zoominevent)
root.bind('<Down>',zoomoutevent)
root.config(menu=menu)
root.mainloop()
