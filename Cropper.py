from ast import Str
import cv2
import numpy as np

def crop(filepath: str):
    image = cv2.imread(filepath)
    original = image.copy()
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (3, 3), 0)
    thresh = cv2.threshold(blurred, 230,255,cv2.THRESH_BINARY_INV)[1]

    # Find contours
    cnts = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    blank = np.zeros(image.shape, dtype="uint8")
    cv2.drawContours(blank, cnts, -1,  (0,0,255), 1)
    blank = cv2.resize(blank,(int(blank.shape[1]*0.2),int(blank.shape[0]*0.2)))
    cv2.imshow('blank',blank)

    # Iterate thorugh contours and filter for ROI
    image_number = 0
    for c in cnts:
        x,y,w,h = cv2.boundingRect(c)
        cv2.rectangle(image, (x, y), (x + w, y + h), (36,255,12), 10)
        if w<20 or h<20:
            continue
        ROI = original[y+1:y+h-1, x+1:x+w-1]
        cv2.imwrite("ROI_{}.png".format(image_number), ROI)
        image_number += 1

    resize = lambda image: cv2.resize(image,(int(image.shape[1]*0.2),int(image.shape[0]*0.2)))

    image = resize(image)
    thresh = resize(thresh)
    cv2.imshow('thresh', thresh)
    cv2.imshow('image', image)
    cv2.waitKey(0)

if __name__ == "__main__":        
    crop('images/test.png')

