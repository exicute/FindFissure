import cv2
import numpy as np
from matplotlib import pyplot as plt
import skimage.exposure as exposure


'''
Две части разработки:
    1) определить hsv параметр для трещины(возможно перебрав все пиксели, можно найти резкий перепад, сравнив между собой несколько соседних)
    2) преобразовать картинку в найденный hsv и разбив его на куски с помощью shape, для каждого куска строить find contours, либо просто использовать findcontours

Первый пунк является основным, т к. позволяет определить цвет трещины, что нам и надо

Разбить картинку на квадратике, просматривать какждый и смотреть сколько в нем цветов, если цветов будет несколько значит в этом квадрате есть трещина

Характеристика поиска трещины:
    1) вокруг трещины имеется контур значение value(v из HSV) которого сильно меньше чем в самой трещине
    2) цвет внутри трещины очень яркий(нужно узнать на сколько)
    3) трещина имеет характерную форму

!!!Решение: просто сгладить картинку(размытие по Гауссу) -> затем применить фильтр Собеля -> найти контуры

'''            

class processedImage():
    def __init__(self, image):
        self.blur = cv2.bilateralFilter(image, 9, 150, 150)
        self.gray = cv2.cvtColor(self.blur, cv2.COLOR_BGR2GRAY)

    def sobel_func(self):
        # apply sobel derivatives
        sobelx = cv2.Sobel(self.blur,cv2.CV_64F,1,0,ksize=3)
        sobely = cv2.Sobel(self.blur,cv2.CV_64F,0,1,ksize=3)
        # square 
        sobelx2 = cv2.multiply(sobelx,sobelx)
        sobely2 = cv2.multiply(sobely,sobely)
        # add together and take square root
        sobel_magnitude = cv2.sqrt(sobelx2 + sobely2)
        # normalize to range 0 to 255 and clip negatives
        self.sobel_magnitude = exposure.rescale_intensity(sobel_magnitude, in_range='image', out_range=(0,255)).clip(0,255).astype(np.uint8)
        return self.sobel_magnitude

    def find_contours(self, filtered_image):
        self.contours, self.hierarchy = cv2.findContours(gray, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE) 
        return self.contours

    def show_image(self):
        cv2.imshow('window', self.blur)
        cv2.waitKey(0)


    

def draw_contours(image, contours):
    cv2.drawContours(image, contours, -1, (0, 255, 0), 2)


if __name__ == "__main__":
    img = cv2.imread('paint0.jpeg')
    my_image = processedImage(img)
    #draw_contours(my_image.blur, my_image.find_contours(my_image.sobel_func()))
    cv2.imshow('window', my_image.sobel_func())
    cv2.waitKey(0)
