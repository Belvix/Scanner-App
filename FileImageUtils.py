import os
import tkinter.filedialog
from PIL import Image, ImageTk
import tkinter 
from vars import *
from components import *

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
    global image_index, zoomin_level, zoomout_level
    image_index+=1
    if image_index==len(images):
        image_index = 0
    zoomin_level = 0
    zoomout_level = 0
    display_image()

def prevImage():
    global image_index, zoomin_level, zoomout_level
    image_index-=1
    if image_index<0:
        image_index = len(images)-1
    zoomin_level = 0
    zoomout_level = 0
    display_image()

def nextImageEvent(event):
    nextImage()

def prevImageEvent(event):
    prevImage()
