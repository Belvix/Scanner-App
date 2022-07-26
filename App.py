from code import compile_command
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
import FileImageUtils as FIU
from vars import *
from components import *

class App(tk.Tk):
    def __init__(self):
        super().__init__()


tk.Grid.rowconfigure(root, 0, weight=1)
tk.Grid.columnconfigure(root, 0, weight=1)

menu.add_cascade(label='File',menu=file)
file.add_command(label="Open", command = FIU.selectmultiplefiles)
menu.add_command(label="newfile", command=None)

middleframe.grid(column=0, row=0, sticky="EW")
middleframe.columnconfigure(0, weight=1)

label.grid(column=0,row=0, rowspan=2, sticky="W")
previousimage.config(command=FIU.prevImage)
previousimage.grid(column=1, row=0, sticky="SE")
nextimage.config(command=FIU.nextImage)
nextimage.grid(column=1,row=1, sticky="NE")
resizerframe.columnconfigure(0, weight=1)
resizerframe.columnconfigure(1, weight=1)
resizerframe.grid(column=0, row=2, sticky="sew")
resizedown.config(command=FIU.zoomout)
resizedown.grid(column=0, row=0, sticky="S")
resizeup.config(command=FIU.zoomin)
resizeup.grid(column=1, row=0, sticky="S")
root.bind('<Up>',FIU.zoominevent)
root.bind('<Down>',FIU.zoomoutevent)
root.bind('<Right>', FIU.nextImageEvent)
root.bind('<Left>',FIU.prevImageEvent)
root.config(menu=menu)
root.mainloop()
