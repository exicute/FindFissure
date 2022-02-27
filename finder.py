import cv2
import numpy as np
from matplotlib import pyplot as plt
import skimage.exposure as exposure


class processedImage():
    def __init__(self, image):
        self.blur = cv2.bilateralFilter(image, 9, 150, 150)
        self.gray = cv2.cvtColor(self.blur, cv2.COLOR_BGR2GRAY)

        # apply sobel derivatives
        sobelx = cv2.Sobel(self.gray,cv2.CV_64F,1,0,ksize=3)
        sobely = cv2.Sobel(self.gray,cv2.CV_64F,0,1,ksize=3)
        # square 
        sobelx2 = cv2.multiply(sobelx,sobelx)
        sobely2 = cv2.multiply(sobely,sobely)
        # add together and take square root
        sobel_magnitude = cv2.sqrt(sobelx2 + sobely2)
        # normalize to range 0 to 255 and clip negatives
        self.sobel_magnitude = exposure.rescale_intensity(sobel_magnitude, in_range='image', out_range=(0,255)).clip(70,255).astype(np.uint8)
        ret, self.thresh = cv2.threshold(self.sobel_magnitude, 128, 255, cv2.THRESH_BINARY)

        kernel = np.ones((8,8), np.uint8)
        self.opening = cv2.morphologyEx(self.thresh, cv2.MORPH_CLOSE, kernel)

        self.contours, self.hierarchy = cv2.findContours(self.opening, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE) 

    def show_image(self):
        cv2.imshow('window', self.blur)
        cv2.waitKey(0)


def delete_defects(item, image):
    for i in range(len(item.contours)-1, 0, -1):
        if cv2.contourArea(item.contours[i])<50:
            continue
        else:
            cv2.drawContours(image, item.contours[i], -1, (0, 255, 0), 2)

    

if __name__ == "__main__":
    img = cv2.imread('paint3.jpeg')
    my_image = processedImage(img)
    delete_defects(my_image, img)
    cv2.imshow('window', img)
    cv2.waitKey(0)
