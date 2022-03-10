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
        
        self.ptA = [(shortSides[0][0][0]+shortSides[0][1][0])//2, (shortSides[0][0][1]+shortSides[0][1][1])//2]
        self.ptB = [(shortSides[1][0][0]+shortSides[1][1][0])//2, (shortSides[1][0][1]+shortSides[1][1][1])//2]



findedLines = []
connectingLines = []


def delete_defects(item, image):
    for i in range(len(item.contours)-1, 0, -1):
        actContour = contourClass(item.contours[i])
        if (actContour.areaLength<80) or ((actContour.arcL)==0 or ((actContour.areaLength)/pow(actContour.arcL, 2))>0.02):
            continue
        else:
            findedLines.append(actContour)
            cv2.drawContours(image, item.contours[i], -1, (0, 255, 0), 2)


def combine_boxes(lines, const):
    for x in range(0, len(lines)-1):
        for y in range(x+1, len(lines)):
            A1 = lines[x].ptA
            A2 = lines[y].ptA
            B1 = lines[x].ptB
            B2 = lines[y].ptB
            alength = np.sqrt((A1[0]-A2[0])**2+(A1[1]-A2[1])**2)
            blength = np.sqrt((B1[0]-B2[0])**2+(B1[1]-B2[1])**2)
            ablength = np.sqrt((B1[0]-A2[0])**2+(B1[1]-A2[1])**2)
            balength = np.sqrt((A1[0]-B2[0])**2+(A1[1]-B2[1])**2)

            if alength<const:
                connectingLines.append([A1, A2])
            if blength<const:
                connectingLines.append([B1, B2])
            if ablength<const:
                connectingLines.append([B1, A2])
            if balength<const:
                connectingLines.append([A1, B2])


def simmilar_var(lines1, lines2, img):
    allLines = [[x.ptA, x.ptB] for x in lines1]
    allLines = allLines+lines2
    allLines = sum(allLines, [])
    
    somepts = []
    endpts = []
    for x in range(0, len(allLines)-1):
        for y in range(x+1, len(allLines)):
            if allLines[x]==allLines[y]:
                somepts.append(allLines[x])

    for x in allLines:
        if x not in somepts:
            endpts.append(x)

    for x in endpts:
        cv2.circle(img, x, 8, (255, 0, 0), 2)
    
    numlines = len(endpts)/2




if __name__ == "__main__":
    img = cv2.imread('paint0.jpeg')
    my_image = processedImage(img)

    delete_defects(my_image, img)
    combine_boxes(findedLines, 50)
    simmilar_var(findedLines, connectingLines, img)
    for l in findedLines:
        cv2.line(img, l.ptA, l.ptB, (0, 0, 255), 2)
    for l in connectingLines:
        cv2.line(img, l[0], l[1], (0, 0, 255), 2)

    cv2.imshow('window', my_image.closing)
    cv2.waitKey(0)
