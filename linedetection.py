__author__ = 'mlm-cs'

import copy
import numpy as np
import cv2
import threading
import csv
from pylab import *
import cv2.cv as cv
import pickle
import copy
import time
import tkintertable

class linedetection(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        # define used kernels
        self.kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
        self.kernel2 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
        self.kernel3 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 4))
        self.kernel5 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2, 4))
        self.flag = 0

        self.initalizeWindows()


    def run(self):
        print 'Line Detection started...'
        while flag:
            self.process()


    def startCamera(self):
        print "Entered to function: startCamera()"
        self.cap = cv2.VideoCapture(0)
        self.cap.set(3, 2560)
        self.cap.set(4, 1920)
        return self.cap

    def initalizeWindows(self):
        cv2.namedWindow('win1', cv2.WINDOW_NORMAL)
        cv2.namedWindow('win2', cv2.WINDOW_NORMAL)
        cv2.namedWindow('win3', cv2.WINDOW_NORMAL)

    def stop(self):
        self.cap.release()
        cv2.destroyAllWindows()

    def process(self):
        print "Entered to function: process()"
        self.cap = self.startCamera()
        ret, self.frame = self.cap.read()
        # Change frame to gray value
        self.gray = cv2.cvtColor(self.frame, cv2.COLOR_RGB2GRAY)
        # cropframe
        self.cropFrame(self.gray)
        cv2.imshow('win3',self.gray)

        clahe = cv2.createCLAHE(clipLimit=5, tileGridSize=(20, 20))
        #clahe = cv2.createCLAHE(clipLimit=1, tileGridSize=(3, 3))   #####ORIGINAL
        self.adapEqualized = clahe.apply(self.gray)
        cv2.imshow('win1', self.adapEqualized)

        self.enhanced = cv2.GaussianBlur(self.adapEqualized, (3, 3), 0)
        self.enhanced = cv2.medianBlur(self.enhanced, 5)
        #cv2.imshow('win1', self.enhanced)

        self.threshold = cv2.adaptiveThreshold(self.enhanced, 235, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 25, 0)  #47
        #cv2.imshow('win1', self.threshold)


        # Morph.

        self.enhanced2 = cv2.GaussianBlur(self.threshold, (7, 13), 0)
        self.enhanced2 = cv2.medianBlur(self.enhanced2, 5)

        ret, self.threshold2 = cv2.threshold(self.enhanced2, 185, 255, cv2.THRESH_BINARY)

        cv2.imshow('win1', self.threshold2)
        #(self.x,self.y) = self.findCenterLaserPoint(self.threshold2)
        #cv2.circle(self.threshold2, (self.x+5,self.y+5), 25,(255,255,255),-1)

        #self.dilation = cv2.dilate(self.threshold2, self.kernel2, iterations=1)
        #self.erotion = cv2.erode(self.dilation, self.kernel, iterations=1)
        #self.opening = cv2.morphologyEx(self.erotion, cv2.MORPH_OPEN, self.kernel5)

        #cv2.imshow('win2',self.erotion)
        #cv2.imshow('win3', self.opening)

        #cv2.imshow('win2', self.threshold2)
        #Copy the image for contour operation
        self.temp = copy.deepcopy(self.threshold2)

        self.contours, self.hierarchy = cv2.findContours(self.temp, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

        self.x = np.ones(np.shape(self.gray)) * 255
        self.tata = np.ones(np.shape(self.gray)) * 255

        self.newcontour = []

        if self.flag != 0:
            for i in np.arange(len(self.contours)):
                if len(self.contours[i]) > 2000:
                    self.newcontour.append(self.contours[i])

            self.newcontour = self.enumerateContours(self.newcontour)

            if len(self.newcontour) > 10:

                # self.straightContour2Line()
                self.objectContour2Line()


                for contour in np.arange(len(self.newcontour)):
                    cv2.drawContours(self.x, self.newcontour[contour], -1, (0, 0, 0), 1)
                    # cv2.waitKey(50)
                    cv2.imshow('win2', self.x)
                    """
                    rows,cols = self.tata.shape[:2]
                    [vx,vy,x,y] = cv2.fitLine(self.newcontour[contour],cv2.cv.CV_DIST_L2,0,0.01,0.01)
                    print   vx
                    print   vy
                    print   x
                    print   y
                    lefty = int((-x*vy/vx) + y)

                    righty = int(((cols-x)*vy/vx)+y)

                    print lefty
                    print righty

                    cv2.line(self.tata,(self.tata.shape[1]-1,righty),(0,lefty),0,1)
                    cv2.imshow('win3',self.tata)
                    """

                # self.createCSV()

        self.flag = 1

        # self.enumcontour = self.enumerateContours(self.newcontour)

        # self.contourToLine()

    def getContours(self):
        return self.newcontour

    def applyFitLine(self):


        pass

    def straightContour2Line(self):
        print "Entered to function: straightContour2Line()"
        self.yAxisLength = np.shape(self.enhanced)[1]
        #print "Length of the Y-Axis: " + str(self.yAxisLength)
        self.cont = self.getContours()
        flag = 0
        # Create empty list to store line information
        self.line = []
        tempY = 0
        #Estimate the centers of the each line contour
        for ithLine in np.arange(len(self.cont)):
            self.line.append([])

            rows, cols = self.tata.shape[:2]
            [vxa, vya, xa, ya] = cv2.fitLine(self.cont[ithLine], cv2.cv.CV_DIST_L2, 0, 0.01, 0.01)

            vxa = vxa[0]
            vya = vya[0]
            x_axis = xa[0]
            y_axis = ya[0]

            pos = [x_axis, y_axis]  #posintion for ---------
            prevPos = [0, 0]
            posTemp = [x_axis, y_axis]
            #print str(ithLine) + ': '
            #print vxa
            #print vya

            for y in np.arange(self.yAxisLength + 250):
                self.tempX = 0
                flag = 0


                #if round(posTemp[1]) == round(pos[1]):
                if pos[0] > 0 and pos[1] <= self.yAxisLength + 1 and pos[1] > 0:


                    if prevPos[1] != round(pos[1]):
                        self.line[ithLine].append([round(pos[0]), round(pos[1])])

                    prevPos[1] = round(pos[1])

                if (pos[1] + vya) >= self.yAxisLength or (pos[1] + vya) <= 0:
                    vxa = -vxa
                    vya = -vya
                    pos = [x_axis, y_axis]
                    posTemp = [x_axis, y_axis]
                    pos[0] += vxa
                    pos[1] += vya
                else:
                    pos[0] += vxa
                    pos[1] += vya

                """
                for  ithPoint in np.arange(len(self.cont[ithLine])):



                    if self.cont[ithLine][ithPoint][0][1] == y:
                        tempy = y
                        self.i += 1
                        self.tempX += self.cont[ithLine][ithPoint][0][0]
                        flag += 1

                    if flag > 5:
                        break


                if self.i != 0:
                    self.line[ithLine].append([self.tempX/self.i, y])
                else:
                    self.line[ithLine].append([0,y])

            print np.shape(self.line)

            with open('output2.txt', 'w') as f:
                for s in self.line:
                    f.write(str(s) + '\n')
                    """

        LineDict = dict(self.line[5])

    def objectContour2Line(self):

        print "Entered to function: objectContour2Line()"
        start = time.time()

        '''
        self.objectLine = []


        self.yAxisLength = np.shape(self.enhanced)[1]

        #Create an iterator which iterates over each line in contour matrix
        self.lineIterator = iter(self.getContours())

        for line in self.lineIterator:


            #Create  an iterator which iterates over each point in a line matrix
            self.pointIterator = iter(line)


            for point in self.pointIterator:
                #Create the an iterator which iterates for y values along y-Axis

                y = iter(np.arange(self.yAxisLength))


                for Point in y:
                    if Point == point[0][1]:
                        a = point[][]


        '''

        self.yAxisLength = np.shape(self.enhanced)[1]
        #print "Length of the Y-Axis: " + str(self.yAxisLength)
        self.cont = self.getContours()
        #print type(self.cont)
        flag = 0

        self.line = []
        #Estimate the centers of the each line contour
        for ithLine in np.arange(len(self.cont)):
            #self.objectline.append([])
            self.line.append([])

            rightsideofLine = {}

            '''
            flag = True
            for ithPoint in self.cont[ithLine]:

                if flag == True:
                    tempY += 1
                elif flag == False:
                    tempY -= 1

                if ithPoint[0][1] == tempY and flag == True:
                    rightsideofLine.update({tempY :ithPoint[0]})
                    self.cont[ithLine].remove(ithPoint)
                    if tempY >len(self.yAxisLength):
                        flag = False
                #elif ithPoint[0][1] == tempY and flag == True:
            '''

            i_1thPoint = [0,0]
            for ithPoint in self.cont[ithLine]:

                if i_1thPoint[1] > ithPoint[0][1]:
                    break
                else:
                    rightsideofLine.update({ithPoint[0][1] :ithPoint[0][0]})

                i_1thPoint = ithPoint[0]

            self.line[ithLine].append(rightsideofLine)



        elapsedTime = time.time() - start
        print 'Elapsed Time for objectContour2Line: ' + str(elapsedTime)
        #self.createCSVLineLocs()




    def getLine(self):
        problem = False
        for ithLine in self.line:
            if len(ithLine[0]) < 1000:
                print   "Some y values are missing..."
                print   "Process Image again"
                problem = True

        if problem == False:
            return self.line
        elif problem == True:
            return False




    def cropFrame(self, frame, section=None):
        # self.gray = frame[section]
        self.gray = frame[230:1750, 500:2475]

    def enumerateContours(self, contours):
        print "Entered to function: enumerateContours()"
        global threshold


        self.centerLineIndex = 0

        enumeratedContours = []
        xLocContour = []
        [xLoc, yLoc] = self.findCenterLaserPoint(self.gray)
        # print str(yLoc) + ' - ' + str(xLoc)

        # copied = copy.deepcopy(contours)

        for ithLine in np.arange(len(contours)):
            flag = True
            for ithPoint in np.arange(len(contours[ithLine])):
                if contours[ithLine][ithPoint][0][1] == yLoc and flag == True:
                    flag = False
                    #print str(ithLine) + '. line located on x axis at point: ' + str(contours[ithLine][ithPoint][0][0])
                    xLocContour.append([contours[ithLine][ithPoint][0][0], ithLine])




        xLocContour.sort()

        #print xLocContour
        for i in np.arange(len(xLocContour)):
            enumeratedContours.append(contours[xLocContour[i][1]])


        Xdiff = []

        for ithline in np.arange(len(enumeratedContours)):
            flag = True
            for ithPoint in np.arange(len(enumeratedContours[ithline])):
                if enumeratedContours[ithline][ithPoint][0][1] == yLoc and flag == True:
                    flag = False
                    # Find the differences between x value of the center point and x-value of the line.
                    diff = abs(enumeratedContours[ithline][ithPoint][0][0] - xLoc)
                    Xdiff.append([diff,ithline])

        self.centerLineIndex  = min(Xdiff)[1]

        return enumeratedContours


    def enumToCenterLine(self):
        self.contours



    def findCenterLaserPoint(self, img):
        print "Entered to function: findCenterLaserPoint()"
        template_size = 20

        template = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (template_size, template_size)) * 255
        result = cv2.matchTemplate(img, template, cv2.TM_SQDIFF_NORMED)


        minVal, maxVal, minLoc, maxLoc = cv2.minMaxLoc(result)

        return minLoc

    def createCSVLineLocs(self):
        t = time.time()

        with open('LineLoc.txt', 'wb') as f:
            writer = csv.writer(f)

            for item in iter(self.line):
                writer.writerow(('######################'))
                writer.writerow(item)

        f.close()
        elapsed = time.time() - t
        print 'Elapsed Time for createCSV: ' + str(elapsed)


    def createCSV(self):

        print "Entered to function: createCSV()"

        #file = open('lines.csv', 'wb')
        #file2 = open('polynomial.csv', 'wb')
        '''
        try:
            for ithLine in np.arange(len(self.line)):
                writer = csv.writer(file)
                writer.writerow(self.newcontour[ithLine])

            #for item in self.line[0]:
               #writer = csv.writer(file)
                #writer.writerow(item)
        finally:
            file.close()
        '''

        t = time.time()

        with open('some.txt', 'wb') as f:
            writer = csv.writer(f)

            for item in iter(self.newcontour):
                writer.writerow(('######################'))
                writer.writerow(item)

        f.close()
        elapsed = time.time() - t
        print 'Elapsed Time for createCSV: ' + str(elapsed)


