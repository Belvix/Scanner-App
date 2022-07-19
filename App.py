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

def changeimage():
    openimage("images/cat.jpg")

def display_image():
    global img, currentimg
    currentimg = images[image_index]
    if currentimg!=None:
        img = ImageTk.PhotoImage(image=currentimg)
        label.configure(image=img)
    else:
        print("Image not loaded")

def addimage(label, image):
    global img
    if image!=None:
        img = ImageTk.PhotoImage(image=image)
        label.configure(image=img)
    else:
        print("Image not loaded")

def selectfiles():
    filepath = tkinter.filedialog.askopenfilenames(initialdir=os.curdir+"/images")
    openimage(filepath[0])

def selectmultiplefiles():
    filepaths = tkinter.filedialog.askopenfilenames(initialdir=os.curdir+"/images")
    openmultipleimages(filepaths)
    
def openimage(filepath):
    global currentimg, images
    images.append(Image.open(filepath))
    print(images)
    currentimg = Image.open(filepath)
    if(currentimg.width > 500 and currentimg.width > currentimg.height):
        ratio = 500/currentimg.width
        print(ratio)
        currentimg = currentimg.resize((500,int(currentimg.height*ratio)))
        print((500,int(500*ratio)))

    elif(currentimg.height > 500 and currentimg.width < currentimg.height):
        ratio = 500/currentimg.width
        currentimg = currentimg.resize((500,int(currentimg.height*ratio)))
    addimage(label, currentimg)


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
    global img, currentimg
    if currentimg!=None:
        image = currentimg.resize((int(currentimg.width*0.9),int(currentimg.height*0.9)))
        img = ImageTk.PhotoImage(image=image)
        currentimg = image
        label.configure(image=img)
    else:
        print("Image not loaded")


def zoomin():
    global img, currentimg
    if currentimg!=None:
        image = currentimg.resize((int(currentimg.width*1.1),int(currentimg.height*1.1)))
        img = ImageTk.PhotoImage(image=image)
        currentimg = image
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
    ...

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
changeimgbtn = ttk.Button(root, text="Change Image", command = changeimage)
changeimgbtn.grid(column=0, row=3, sticky="NSEW")
resizedown = ttk.Button(resizerframe, text="Zoom Out", command = lambda: zoomout())
resizedown.grid(column=0, row=0, sticky="S")
resizeup = ttk.Button(resizerframe, text="Zoom In", command = lambda: zoomin())
resizeup.grid(column=1, row=0, sticky="S")
root.bind('<Up>',zoominevent)
root.bind('<Down>',zoomoutevent)
root.config(menu=menu)
root.mainloop()
