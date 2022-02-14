import cv2
from PIL import Image as Img
from PIL import ImageTk
from tkinter import *
from tkinter import filedialog
import numpy as np
import sys
import random as rng
import tempfile
import os



class App:

    def __init__(self, window, window_title='None'):

        self.window = window
        self.window.title(window_title)
        self.wait_time = 33

    # Initialize to check if HSV min/max value changes
        self.hMin = self.sMin = self.vMin = self.hMax = self.sMax = self.vMax = 0
        self.phMin = self.psMin = self.pvMin = self.phMax = self.psMax = self.pvMax = 0

    # Create a canvas that can fit the above image
        self.canvas1 = Canvas(window, width = 600, height = 350)
        self.canvas1.pack()

        self.w1 = Scale(self.window, from_=0, to=179, label='hMin', orient=HORIZONTAL, length=600)
        self.w1.set(0)
        self.w1.pack()
        self.w2 = Scale(self.window, from_=0, to=255, label='sMin', orient=HORIZONTAL, length=600)
        self.w2.set(0)
        self.w2.pack()
        self.w3 = Scale(self.window, from_=0, to=255, label='vMin', orient=HORIZONTAL, length=600)
        self.w3.set(0)
        self.w3.pack()
        self.w4 = Scale(self.window, from_=0, to=179, label='hMax', orient=HORIZONTAL, length=600)
        self.w4.set(179)
        self.w4.pack()
        self.w5 = Scale(self.window, from_=0, to=255, label='sMax', orient=HORIZONTAL, length=600)
        self.w5.set(255)
        self.w5.pack()
        self.w6 = Scale(self.window, from_=0, to=255, label='vMax', orient=HORIZONTAL, length=600)
        self.w6.set(255)
        self.w6.pack()

        self.label = Label(text='0', compound='center', font=16, fg='#eee', bg='#ffaaaa')
        self.label.pack(side=BOTTOM)

        self.btn2 = Button(self.window, text="box", command=self.Contour)
        self.btn2.pack()
        self.load_btn = Button(self.window, text="load", command=self.load_img)
        self.load_btn.pack(side=LEFT)
        self.save_btn = Button(self.window, text="save", command=self.save_img)
        self.save_btn.pack(side=RIGHT)
        
        self.pool = False
        while True:
            try:
                if self.pool == False:
                    self.main_image()
                else: 
                    self.TrackBar()
                    self.draw_window()
            except TclError:
                break

        self.window.mainloop()


    def main_image(self):
        self.image_path = filedialog.askopenfilename()
        self.cv_img = cv2.imread(self.image_path)
        self.hsv = cv2.cvtColor(self.cv_img, cv2.COLOR_BGR2HSV)
        self.pool = True


    def draw_window(self):

        # Set minimum and max HSV values to display
        self.lower = np.array([self.hMin, self.sMin, self.vMin], dtype='uint8')
        self.upper = np.array([self.hMax, self.sMax, self.vMax], dtype='uint8')

        # Create HSV Image and threshold into a range.
        self.mask = cv2.inRange(self.hsv, self.lower, self.upper)
        self.output = cv2.bitwise_and(self.cv_img, self.cv_img, mask= self.mask)

        #Use PIL (Pillow) to convert the NumPy ndarray to a PhotoImage
        self.photo = ImageTk.PhotoImage(image = Img.fromarray(self.output).resize((600, 350)))

        # Add a PhotoImage to the Canvas
        self.canvas1.create_image(0, 0, image=self.photo, anchor=NW)
        self.window.update()
#            self.window.after(10, self.draw_window)


    def TrackBar(self):

        self.hMin = self.w1.get()
        self.sMin = self.w2.get()
        self.vMin = self.w3.get()
        self.hMax = self.w4.get()
        self.sMax = self.w5.get()
        self.vMax = self.w6.get()
    # Print if there is a change in HSV value
        if( (self.phMin != self.hMin) | (self.psMin != self.sMin) | (self.pvMin != self.vMin) | (self.phMax != self.hMax) | (self.psMax != self.sMax) | (self.pvMax != self.vMax) ):
            print("(hMin = %d , sMin = %d, vMin = %d), (hMax = %d , sMax = %d, vMax = %d)" % (self.hMin , self.sMin , self.vMin, self.hMax, self.sMax , self.vMax))
            self.phMin = self.hMin
            self.psMin = self.sMin
            self.pvMin = self.vMin
            self.phMax = self.hMax
            self.psMax = self.sMax
            self.pvMax = self.vMax
#            self.window.after(10, self.TrackBar)


    def Contour(self):
        self.contours, self.hierarchy = cv2.findContours(self.mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE) 

        for i in range(len(self.contours)-1, 0, -1):
            if cv2.contourArea(self.contours[i])<50:
                del(self.contours[i])
            else:
                continue

        for i in range(len(self.contours)-1, 0, -1):
            if (cv2.arcLength(self.contours[i], True))==0 or ((cv2.contourArea(self.contours[i])/pow(cv2.arcLength(self.contours[i], True), 2))>0.02):
                del(self.contours[i])
            else:
                continue

        self.end_contours = self.contours
        cv2.drawContours(self.cv_img, self.contours, -1, (0, 255, 0), 2)

        self.label.config(text=len(self.end_contours))


    def load_img(self):
        self.pool = False


    def save_img(self):
        Img.fromarray(self.output).save(tempfile.NamedTemporaryFile(mode='w', suffix='.jpeg', dir=os.getcwd()).name)
        print(os.getcwd())
        print(tempfile.NamedTemporaryFile(mode='w', suffix='.jpeg').name)




if __name__ == "__main__":
    MyApp = App(Tk())
    print("(hMin = %d , sMin = %d, vMin = %d), (hMax = %d , sMax = %d, vMax = %d)" % (MyApp.hMin , MyApp.sMin , MyApp.vMin, MyApp.hMax, MyApp.sMax , MyApp.vMax))
    print(len(MyApp.end_contours))
