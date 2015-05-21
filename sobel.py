__author__ = 'mlm-cs'
import copy

import numpy as np
import cv2
import threading
import tkintertable
from Tkinter import *
import logging

import cv2.cv as cv
from Tkinter import *

# Helper Functions
def hist_lines(im):
    h = np.zeros((300,256,3))
    hist_item = cv2.calcHist([im], [0], None, [256], [0, 256])
    cv2.normalize(hist_item,hist_item,0,255,cv2.NORM_MINMAX)
    hist=np.int32(np.around(hist_item))
    for x , y in enumerate(hist):
        cv2.line(h, (x, 0), (x, y), (255, 255,255))
    y = np.flipud(h)
    return y

def takeInfo(event, x, y, flags, param):
    global x1, x2, y1 , y2
    if event == cv2.EVENT_LBUTTONDOWN:
        x1 = x
        y1 = y
        print 'XPos: ' + str(x)
        print 'YPos: ' + str(y)


    elif event == cv2.EVENT_LBUTTONUP:
        x2 = x
        y2 = y
        print 'XPos: ' + str(x)
        print 'YPos: ' + str(y)

def nothing(x):
    pass

def findCenterLaserPoint(img):
    #kernel = np.ones((kernel_size, kernel_size), np.float32) / (float)(kernel_size*kernel_size)
    #kernel[kernel_size/2, kernel_size/2] = np.zeros((5, 5), np.float32) / (float)(5*5)
    #filtered = cv2.filter2D(img, -1, kernel)
    #cv2.imshow('asdas', filtered)
    #template = np.ones((template_size, template_size), np.uint8) * 255
    template_size = 50
    template = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (template_size,template_size)) * 255
    result = cv2.matchTemplate(img, template,cv2.TM_SQDIFF_NORMED)
    minVal, maxVal, minLoc, maxLoc = cv2.minMaxLoc(result)
    #cv2.imshow('Finding center Laser Point', result)
    return minLoc

def CenterThreshold(img):
    clahe = cv2.createCLAHE(clipLimit=4, tileGridSize=(4,4))
    dst = clahe.apply(img[650:800, 1125:1275])
    re, dst = cv2.threshold(dst, 253, 255, cv2.THRESH_BINARY_INV)
    dst = cv2.GaussianBlur(dst, (11,11),0 )
    re, dst = cv2.threshold(dst, 253, 255, cv2.THRESH_BINARY)
    return dst

def ApplyFilter(img):
    filterKernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7,7)) * -0.1/49.0
    filterKernel[4,4] = 1.0
    dst = cv2.filter2D(img[1150:1250, 685:785], -1, filterKernel)
    img[1150:1250, 685:785] = dst
    return img

def AproxPoly(contours):
    approxCurve = []
    for i in np.arange(len(contours)):
        approxCurve.append(cv2.approxPolyDP(contours[i], epsilon = 5, closed = False))

    return approxCurve

#Finds the y point of the center laser point and enumerates the lines along x-axis
def enumerateContours(contours):
    global enhanced
    enumeratedContours = []
    xLocContour = []
    [xLoc, yLoc] = findCenterLaserPoint(enhanced)
    print str(yLoc) + ' - ' + str(xLoc)
    copied = copy.deepcopy(contours)

    for ithLine in np.arange(len(contours)):
        flag = True
        for  ithPoint in np.arange(len(contours[ithLine])):
            if contours[ithLine][ithPoint][0][1] == yLoc and flag == True:
                flag = False
                print str(ithLine) + '. line located on x axis at point: ' + str(contours[ithLine][ithPoint][0][0])
                xLocContour.append([contours[ithLine][ithPoint][0][0], ithLine])

    xLocContour.sort()
    print xLocContour
    for i in np.arange(len(xLocContour)):
       enumeratedContours.append(contours[xLocContour[i][1]])

    return enumeratedContours

logging.debug('Program starts')



#Initilaze camera to and resulation
cap = cv2.VideoCapture(0)
cap.set(3,2560)
cap.set(4,1920)

#####################################################################################
#Initlize needed windows
cv2.namedWindow('Original Image', cv2.WINDOW_NORMAL)
cv2.namedWindow('Contours', cv2.WINDOW_NORMAL)
#cv2.namedWindow('asdas', cv2.WINDOW_NORMAL)
#cv2.namedWindow('Threshold' , cv2.WINDOW_NORMAL)
#cv2.namedWindow('Morpho.', cv2.WINDOW_NORMAL)
#cv2.namedWindow('Filter 2D Demo' , cv2.WINDOW_NORMAL)
cv2.namedWindow('Image Enhancement 2', cv2.WINDOW_NORMAL)

y1 = 500
cv2.setMouseCallback('Image Enhancement 2', takeInfo)
flag = 0
#######################################################################################
#######################################################################################
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3,3))
kernel2 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5,5))
kernel3 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3,4))
kernel5 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2,4))
blocksizeArray = np.arange(3,101, 2)
######################---------------Main loop--------------###########################
while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    #Set up mouse Callback


    # Change frame to gray value
    gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
    #Copy the image
    gray = gray[230:1750, 500:2475]


    #rows, cols = gray.shape
    #M = cv2.getRotationMatrix2D((cols/2, rows/2) , -90, 1)
    #gray = cv2.warpAffine(gray, M, (cols, rows))

    #Adaptive Histogram Equalization using CLAHE
    clahe = cv2.createCLAHE(clipLimit=1, tileGridSize=(3,3))
    adapEqualized = clahe.apply(gray)


###############################################################
########     Image Enhancement
    enhanced = cv2.GaussianBlur(adapEqualized, (3,3),0)
    enhanced = cv2.medianBlur(enhanced, 15)

    #centerLoc = findCenterLaserPoint(enhanced)
    #[Xmax, Ymax] = findCenterLaserPoint(enhanced)
    #print Xmax
    #print Ymax
    #maxVal, maxLoc  = findCenterLaserPoint(enhanced)
    #print maxVal
    #print maxLoc[0]
    #print maxLoc[1]
    #cv2.circle(enhanced, maxLoc , 10, (0,0,0), -1 )


    # Adaptive Threshold the image
    threshold = cv2.adaptiveThreshold(enhanced, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 47 ,0)

    # Morph.
    opening = cv2.morphologyEx(threshold, cv2.MORPH_OPEN, kernel2)

    enhanced2 = cv2.GaussianBlur(opening, (7,5) ,0)
    enhanced2 = cv2.medianBlur(enhanced2, 5)
    erosion2 = cv2.erode(enhanced2, kernel, iterations=1)

    ret, threshold2 = cv2.threshold(erosion2,200, 255, cv2.THRESH_BINARY)


    #cv2.circle(erosion3, (maxLoc[0], maxLoc[1] + 25) , 50, (255,255,255), -1 )
    #Copy the image for contour operation
    temp = copy.deepcopy(threshold2)

    contours, hierarchy = cv2.findContours(temp ,cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE )

    x = np.ones(np.shape(gray)) * 255

    newcontour = []

    if flag != 0:
        for i in np.arange(len(contours)):
            if len(contours[i]) > 500:
                newcontour.append(contours[i])

        newcontour = enumerateContours(newcontour)

        if len(newcontour) > 5:
            for contour in np.arange(len(newcontour)):
                cv2.drawContours(x, newcontour[contour], -1,(0,0,0), 3)
                cv2.waitKey(250)
                cv2.imshow('Contours', x)
    flag = 1

    enumerateContours(newcontour)
    #closing = cv2.morphologyEx(x, cv2.MORPH_OPEN, kernel2)
    #x = x.astype(np.uint8)
    #ret, threshold2 = cv2.threshold(x,200, 255, cv2.THRESH_BINARY_INV)
    #closing = cv2.dilate(threshold2, kernel, iterations=8)
    #closing = cv2.erode(closing, kernel, iterations=9)
    #closing = cv2.erode(closing, kernel5, iterations=1)

    #contours2, hierarchy = cv2.findContours(closing ,cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE )

###################################################################
    # Show corresponding windows
    cv2.imshow('Original Image', gray)
    cv2.imshow('Image Enhancement 2', enhanced)
    #cv2.imshow('Threshold', threshold3)
    #cv2.imshow('Morpho.', threshold)
    #v2.imshow('Blob', blob)
    #cv2.imshow('Adaptive Thresholded Image', thresGray2)
    #cv2.imshow('MedianBlured', thresGray3)
########################################################################

########################################################################
    #Check for an exit key
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

#########################################################################



# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
