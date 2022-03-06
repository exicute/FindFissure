import cv2 
import numpy as np
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
        self.sobel_magnitude = exposure.rescale_intensity(sobel_magnitude, in_range='image', out_range=(0,255)).clip(80,255).astype(np.uint8)
        ret, self.thresh = cv2.threshold(self.sobel_magnitude, 140, 255, cv2.THRESH_BINARY)

        kernel = np.ones((5,5), np.uint8)
        self.opening = cv2.morphologyEx(self.thresh, cv2.MORPH_CLOSE, kernel)

        self.contours, self.hierarchy = cv2.findContours(self.opening, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE) 

    def show_image(self):
        cv2.imshow('window', self.blur)
        cv2.waitKey(0)
