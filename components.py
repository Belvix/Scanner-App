import tkinter as tk
from tkinter import ttk

root = tk.Tk()

menu = tk.Menu(root)
file = tk.Menu(menu,tearoff=0)
middleframe = tk.Frame(root, highlightbackground="black", highlightthickness=2, relief=tk.SUNKEN)
label = ttk.Label(middleframe,text='No Image' ,image = None)
resizerframe = tk.Frame(root, highlightbackground="black", highlightthickness=2, relief=tk.SUNKEN)
previousimage = ttk.Button(middleframe, text="Prev")
nextimage = ttk.Button(middleframe, text="Next")
resizedown = ttk.Button(resizerframe, text="Zoom Out")
resizeup = ttk.Button(resizerframe, text="Zoom In")
