import cv2
import numpy as np
import skimage.exposure as exposure

# read the image
img = cv2.imread('paint3.jpeg')
img = cv2.resize(img, (1920, 1080))

# convert to gray
gray = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)

# blur
blur = cv2.GaussianBlur(gray, (0,0), 1.3, 1.3)

# apply sobel derivatives
sobelx = cv2.Sobel(blur,cv2.CV_64F,1,0,ksize=3)
sobely = cv2.Sobel(blur,cv2.CV_64F,0,1,ksize=3)

# optionally normalize to range 0 to 255 for proper display
sobelx_norm= exposure.rescale_intensity(sobelx, in_range='image', out_range=(0,255)).clip(0,255).astype(np.uint8)
sobely_norm= exposure.rescale_intensity(sobelx, in_range='image', out_range=(0,255)).clip(0,255).astype(np.uint8)

# square 
sobelx2 = cv2.multiply(sobelx,sobelx)
sobely2 = cv2.multiply(sobely,sobely)

# add together and take square root
sobel_magnitude = cv2.sqrt(sobelx2 + sobely2)

# normalize to range 0 to 255 and clip negatives
sobel_magnitude = exposure.rescale_intensity(sobel_magnitude, in_range='image', out_range=(0,255)).clip(0,255).astype(np.uint8)

# save results
cv2.imwrite('gray_lena_sobelx_norm.jpg', sobelx_norm)
cv2.imwrite('gray_lena_sobely_norm.jpg', sobely_norm)
cv2.imwrite('gray_lena_sobel_magnitude.jpg', sobel_magnitude)

# show results
cv2.imshow('sobelx_norm', sobelx_norm)  
cv2.imshow('sobely_norm', sobely_norm)  
cv2.imshow('sobel_magnitude', sobel_magnitude)  
cv2.waitKey(0)
cv2.destroyAllWindows() 