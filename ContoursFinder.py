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
        self.weight = shortSides[0][2]
        self.length = np.sqrt((self.ptA[0]-self.ptB[0])**2+(self.ptA[1]-self.ptB[1])**2)

        self.friends = {'a':'', 'b':'', 'ab':'', 'ba':''}



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
                lines[x].friends['a'] = [alength, lines[y]]
            if blength<const:
                connectingLines.append([B1, B2])
                lines[x].friends['b'] = [blength, lines[y]]
            if ablength<const:
                connectingLines.append([B1, A2])
                lines[x].friends['ab'] = [ablength, lines[y]]
            if balength<const:
                connectingLines.append([A1, B2])
                lines[x].friends['ba'] = [balength, lines[y]]


somepts = []

def simmilar_var(lines1, lines2, img):
    allLines = [[x.ptA, x.ptB] for x in lines1]
    allLines = allLines+lines2
    allLines = sum(allLines, [])
    
    allpts = []
    endpts = []
    for x in range(0, len(allLines)-1):
        ptsX = []
        for y in range(x+1, len(allLines)):
            if allLines[x]==allLines[y]:
                ptsX.append(allLines[x])
                allpts.append(allLines[x])
        if len(ptsX)>0:
            somepts.append(ptsX)

    for x in allLines:
        if x not in allpts:
            endpts.append(x)


    for x in endpts:
        cv2.circle(img, x, 8, (255, 0, 0), 2)
    
    numlines = len(endpts)/2



def length_finder(pts, img):
    lines = pts

    for x in lines:
        elmts = []
        length = x.length
        
        for key in x.friends.keys():
            if x.friends[key]!='':
                length+=x.friends[key][0]
                elmts.append(x.friends[key][1])

        while True:
            if len(elmts)>0:
                print('')
                print(len(elmts))
                for y in elmts:
                    length+=y.length
                    for key in y.friends.keys():
                        if y.friends[key]!='':
                            length+=y.friends[key][0]
                            elmts.append(y.friends[key][1])
                    elmts.remove(y)
                    if y in lines:
                        print(y)
                        lines.remove(y)

            else:
                break
        cv2.putText(img, '{:.0f}'.format(length), (x.ptA[0], x.ptA[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 255), 2)
        cv2.putText(img, '{:.0f}'.format(x.weight), (x.ptA[0]+30, x.ptA[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 255), 2)
    




if __name__ == "__main__":
    img = cv2.imread('paint3.jpeg')
    my_image = processedImage(img)

    delete_defects(my_image, img)
    combine_boxes(findedLines, 30)
    simmilar_var(findedLines, connectingLines, img)
    for l in findedLines:
        cv2.line(img, l.ptA, l.ptB, (0, 0, 255), 2)
    for l in connectingLines:
        cv2.line(img, l[0], l[1], (0, 0, 255), 2)

    length_finder(findedLines, img)

    cv2.imshow('window', img)
    cv2.waitKey(0)
