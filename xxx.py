__author__ = 'mlm-cs'
import numpy as np
import cv2
import copy
import scipy
import cv2.cv as cv


# Functions
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
        print closing3xxxxxx[y,x]

    elif event == cv2.EVENT_LBUTTONUP:
        x2 = x
        y2 = y
        print 'XPos: ' + str(x)
        print 'YPos: ' + str(y)
        print closing3xxxxxx[y,x]

def nothing(x):
    pass

def findCenterLaserPoint(img):
    minVal, maxVal, minLoc, maxLoc = cv2.minMaxLoc(img)

    return maxVal, maxLoc

def CenterThreshold(img):
    clahe = cv2.createCLAHE(clipLimit=4, tileGridSize=(4,4))
    dst = clahe.apply(img[650:800, 1125:1275])
    re, dst = cv2.threshold(dst, 253, 255, cv2.THRESH_BINARY_INV)
    dst = cv2.GaussianBlur(dst, (11,11),0 )
    re, dst = cv2.threshold(dst, 253, 255, cv2.THRESH_BINARY)
    return dst

filterKernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7,7)) * -0.1/49.0
filterKernel[4,4] = 1.0
def ApplyFilter(img):
    dst = cv2.filter2D(img[1150:1250, 685:785], -1, filterKernel)
    img[1150:1250, 685:785] = dst
    return img


def AproxPoly(contours):
    approxCurve = []
    for i in np.arange(len(contours)):
        approxCurve.append(cv2.approxPolyDP(contours[i], epsilon = 5, closed = False))

    return approxCurve

def enumarateContours(contours):


    pass

#Initilaze camera to and resulation
cap = cv2.VideoCapture(0)
cap.set(3,2560)
cap.set(4,1920)

#####################################################################################
#Initlize needed windows
cv2.namedWindow('Original Image', cv2.WINDOW_NORMAL)
cv2.namedWindow('Contours', cv2.WINDOW_NORMAL)
#cv2.namedWindow('Blob', cv2.WINDOW_NORMAL)
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
kernel3 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (6,6))

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
    enhanced = cv2.medianBlur(enhanced, 3)



    maxVal, maxLoc  = findCenterLaserPoint(enhanced)
    #print maxVal
    #print maxLoc[0]
    #print maxLoc[1]
    cv2.circle(gray, maxLoc , 10, (0,0,0), -1 )

    img = copy.deepcopy(enhanced)
    img = CenterThreshold(img)

    # Adaptive Threshold the image
    threshold = cv2.adaptiveThreshold(enhanced, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 47 ,0)

    # Morph.
    closing2 = cv2.morphologyEx(threshold, cv2.MORPH_ELLIPSE, kernel)
    closingx2 = cv2.morphologyEx(closing2, cv2.MORPH_ELLIPSE, kernel)
    closingxx2 = cv2.morphologyEx(closingx2, cv2.MORPH_ELLIPSE, kernel)
    closingxxx2 = cv2.morphologyEx(closingxx2, cv2.MORPH_ELLIPSE, kernel)
    opening2 = cv2.morphologyEx(closingxxx2, cv2.MORPH_ELLIPSE, kernel2)


    enhanced2 = cv2.GaussianBlur(opening2, (9,5) ,0)
    enhanced2 = cv2.medianBlur(enhanced2, 13)
    ret, threshold2 = cv2.threshold(enhanced2, 230, 255, cv2.THRESH_BINARY)
    #threshold2 = cv2.adaptiveThreshold(enhanced2, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 25 ,0)
    dilation = cv2.erode(threshold2, kernel, iterations=8)
    erosion = cv2.dilate(dilation, kernel, iterations=12)
    enhanced3 = cv2.GaussianBlur(erosion, (17, 21) ,0)
    #ret, threshold3 = cv2.threshold(enhanced3, 230, 255, cv2.THRESH_BINARY)
    threshold3 = cv2.adaptiveThreshold(enhanced3, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 45 ,0)
    #dilation2 = cv2.erode(threshold3, kernel, iterations=8)

    closing3 = cv2.morphologyEx(threshold3, cv2.MORPH_ELLIPSE, kernel)
    closing3x = cv2.morphologyEx(closing3, cv2.MORPH_ELLIPSE, kernel2)
    closing3xx = cv2.morphologyEx(closing3x, cv2.MORPH_ELLIPSE, kernel2)
    closing3xxx = cv2.morphologyEx(closing3xx, cv2.MORPH_ELLIPSE, kernel)
    closing3xxxx = cv2.morphologyEx(closing3xxx, cv2.MORPH_ELLIPSE, kernel)
    closing3xxxxx = cv2.morphologyEx(closing3xxxx, cv2.MORPH_ELLIPSE, kernel)
    closing3xxxxxx = cv2.morphologyEx(closing3xxxxx, cv2.MORPH_ELLIPSE, kernel)


    ret, threshold4 = cv2.threshold(closing3xxxxxx,200, 255, cv2.THRESH_BINARY_INV)

    erosion3 = cv2.erode(threshold4, kernel2, iterations=1)



    cv2.circle(erosion3, (maxLoc[0], maxLoc[1] + 25) , 50, (255,255,255), -1 )
    #Copy the image for contour operation
    temp = copy.deepcopy(erosion3)

    contours, hierarchy = cv2.findContours(temp ,cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE )

    x = np.ones(np.shape(gray)) * 255

    newcontour = []

    for i in np.arange(len(contours)):
        if len(contours[i]) > 500:
            newcontour.append(contours[i])


    if len(newcontour) > 5:
        for contour in np.arange(len(newcontour)):
            cv2.drawContours(x, newcontour[contour], -1,(0,255,0), 3)

            cv2.waitKey(250)
            cv2.imshow('Contours', x)

    #print np.shape(newcontour[1])
###################################################################
    # Show corresponding windows
    cv2.imshow('Original Image', gray)
    cv2.imshow('Image Enhancement 2', threshold)
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