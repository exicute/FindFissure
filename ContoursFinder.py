import cv2 
import numpy as np
from matplotlib import pyplot as plt
import skimage.exposure as exposure
from ImageLoad import processedImage



class contourClass():
    def __init__(self, contour):
        self.areaLength = cv2.contourArea(contour)
        self.arcL = cv2.arcLength(contour, True)

        rect = cv2.minAreaRect(contour)
        box = cv2.boxPoints(rect)
        box = np.int0(box)

       #coordinats: 4 corners(longSideA, longSideB, shortSideA, shortSideB), large midlane(ptA, ptB)
        allSidesInfo = []
        shortSides = []
        lines = []

        for x in range(0, 3):
           for y in range(x+1, 4):
               lineLength = np.sqrt((box[x][0]-box[y][0])**2+(box[x][1]-box[y][1])**2)
               allSidesInfo.append([box[x], box[y], lineLength])
               lines.append(lineLength)

        mins = []
        for x in range(2):
            mins.append(min(lines))
            lines.remove(min(lines))

        for m in mins:
            for side in allSidesInfo:
                if side[2]==m:
                    shortSides.append(side)
        
        #print(shortSides)
        #print("+" + '\n')
        self.ptA = [(shortSides[0][0][0]+shortSides[0][1][0])//2, (shortSides[0][0][1]+shortSides[0][1][1])//2]
        self.ptB = [(shortSides[1][0][0]+shortSides[1][1][0])//2, (shortSides[1][0][1]+shortSides[1][1][1])//2]



allLines = []

def delete_defects(item, image):
    for i in range(len(item.contours)-1, 0, -1):
        actContour = contourClass(item.contours[i])
        if (actContour.areaLength<80) or ((actContour.arcL)==0 or ((actContour.areaLength)/pow(actContour.arcL, 2))>0.02):
            continue
        else:
            allLines.append([actContour.ptA, actContour.ptB, actContour])
            cv2.drawContours(image, item.contours[i], -1, (0, 255, 0), 2)


def combine_boxes():
    pass

    

if __name__ == "__main__":
    img = cv2.imread('paint0.jpeg')
    my_image = processedImage(img)
    delete_defects(my_image, img)
    print(allLines)
    for l in allLines:
        cv2.line(img, l[0], l[1], (0, 0, 255), 2)

    cv2.imshow('window', img)
    cv2.waitKey(0)
