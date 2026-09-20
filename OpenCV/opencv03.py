import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt

def resize(frame,scale=0.2):
    width = int(frame.shape[1]*scale)
    height = int(frame.shape[0]*scale)
    dimensions = (width,height)
    return cv.resize(frame,dimensions,interpolation =cv.INTER_AREA)
img = cv.imread('/home/yogendra/Documents/AIEngineer/OpenCV/manja-vitolic-gKXKBY-C-Dk-unsplash.jpg')
resize = resize(img)

# COMPUTING HISTOGRAM --------------------------

# gray = cv.cvtColor(resize,cv.COLOR_BGR2GRAY)
# blank= np.zeros(resize.shape[:2],dtype = 'uint8')
# circle = cv.circle(blank,(resize.shape[1]//2,resize.shape[0]//2),100,255,-1)
# mask = cv.bitwise_and(gray,gray,mask=circle)
# gray_hist = cv.calcHist([gray],[0],mask,[256],[0,256]) # (image, channel Number, Mask, Number of bins, range of bins that will show on image)
# plt.figure()
# plt.title('Histogram of pixcels')
# plt.xlabel('Bin')
# plt.ylabel('no of pixels')
# plt.plot(gray_hist)
# plt.xlim([0,256])
# plt.show()
# cv.imshow('Gray',gray)
# cv.imshow('Mask',mask)
# cv.waitKey(0)

# THRESHOLDING------------------------------------

gray = cv.cvtColor(resize,cv.COLOR_BGR2GRAY)
threshold,thresh = cv.threshold(gray,125,255,cv.THRESH_BINARY) # (src image, if pixels <125 assign black(0), above 125 assign white(1))
adaptive_thresh = cv.adaptiveThreshold(gray,255,cv.ADAPTIVE_THRESH_MEAN_C,cv.THRESH_BINARY_INV,11,3)
# cv.imshow('Adaptive_Thresh',adaptive_thresh)
# cv.imshow('Simple Thresholded',thresh)


# EDGE DETECTION----------------------------------

lap = cv.Laplacian(gray,cv.CV_64F)
lap = np.uint8(np.absolute(lap))
sobelx = cv.Sobel(gray,cv.CV_64F,1,0)
sobely = cv.Sobel(gray,cv.CV_64F,0,1)
combined = cv.bitwise_or(sobelx,sobely)
canny = cv.Canny(gray,150,175)
cv.imshow('Laplacian',lap)
cv.imshow('Sobel X',sobelx)
cv.imshow('Sobel Y', sobely)
cv.imshow('Combined',combined)
cv.imshow('Canny',canny)
cv.waitKey(0)