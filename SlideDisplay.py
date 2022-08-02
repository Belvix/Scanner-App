from sys import displayhook
import tkinter as tk
from PIL import Image, ImageTk
from ScannerImage import ScannerImage

class SlideDisplay(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, highlightbackground="blue", highlightthickness=2, width=220, height=651)
        self.image_list: list[ImageTk.PhotoImage] = list()
        self.label_list: list[tk.Label] = list()
        self.width: list[int] = list()

        self.scrollval = 0

    def scroll(self, direction):
        if(self.scrollval>0):
            if(direction>0):
                self.scrollval-=1
        if(direction<0):
            self.scrollval+=1
        print(self.scrollval)
        self.display_labels()

    def add_image_and_label(self, image: ScannerImage):
        self.image_list.append(image)
        self.label_list.append(tk.Label(self, image=image.thumbnail_image, bd=2, relief="sunken"))
        self.width.append(image.thumbnail_image.width())
        self.display_labels()

    def create_image_labels(self, list: list[ScannerImage]):
        self.image_list = list
        for image in self.image_list:
            self.label_list.append(tk.Label(self, image=image.thumbnail_image, bd=2, relief="sunken"))
            self.width.append(image.thumbnail_image.width())

        self.display_labels()

    def reset(self):
        self.width: list[int] = list()
        for i in self.label_list:
            i.place_forget()
        self.label_list: list[tk.Label] = list()
        self.image_list: list[ImageTk.PhotoImage] = list()
        self.display_labels()
    
    def display_labels(self):
        print(len(self.label_list))
        for i, label in enumerate(self.label_list):
            label.place(x= 5+100-(self.width[i]//2), y= 10+100*i+10*i+(20*self.scrollval))
