import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt

# Function to resize the image. 
def resize(img,scale = 0.2):
    height = int(img.shape[0]*scale)
    width =  int(img.shape[1]*scale)
    dimensions = (width,height)
    return cv.resize(img,dimensions,interpolation=cv.INTER_AREA)

# COLOR SPACES----------------------------------

img = cv.imread('/home/yogendra/Documents/AIEngineer/OpenCV/manja-vitolic-gKXKBY-C-Dk-unsplash.jpg')
resized_img = resize(img)
# gray = cv.cvtColor(resized_img,cv.COLOR_BGR2GRAY)
# Hsv = cv.cvtColor(resized_img,cv.COLOR_BGR2HSV) # HSV(Heu Saturation Value) it is used to represent the color how human perceive the color, Hue = what color is it?,saturation  = how much pixels present in that range, Value = brightness., color order Red → Yellow → Green → Cyan → Blue → Magenta → Red
# Lab = cv.cvtColor(resized_img,cv.COLOR_BGR2LAB)
# cv.imshow('Image',resized_img)
# cv.waitKey(0)
# # cv.imshow('Gray Image',gray)
# cv.imshow('HSV Image',Hsv)
# cv.imshow("Lab Image",Lab)
# plt.imshow(resized_img)
# plt.show()
# # cv.waitKey(0)

# COLOR CHANNELS -------------------------------

# b,g,r = cv.split(resized_img)
# blank = np.zeros(resized_img.shape[:2],dtype = 'uint8')
# blue = cv.merge([b,blank,blank])
# green= cv.merge([blank,g,blank])
# red =  cv.merge([blank,blank,r])
# merged=cv.merge([b,g,r])
# cv.imshow('Blue',b)
# cv.imshow('Green',g)
# cv.imshow('Red',r)
# cv.imshow('Blue1',blue)
# cv.imshow('Green1',green)
# cv.imshow('Red1',red)
# cv.imshow('merged',merged)
# cv.waitKey(0)
# print(resized_img.shape)
# print(b.shape)
# print(g.shape)
# print(r.shape)

# BLURRING TECHNIQUES

# first method of blur is averaging
# blur=cv.GaussianBlur(resized_img,(7,7),cv.BORDER_DEFAULT) # (7,7) is kernel size that will follow on an image and will calculate average and assign the average value in replace the pixels value
# average = cv.blur(resized_img,(7,7))
# median = cv.medianBlur(resized_img,3) # I wrote 3 means it will automatically assign kernel size is (3,3)
# bilatral = cv.bilateralFilter(resized_img,7,23,69)
# cv.imshow('Bilatral_img',bilatral)
# cv.imshow('Median_clur',median)
# cv.imshow('Blur',blur)
# cv.imshow('Averaged_blur',average)
# cv.waitKey(0)

# BITWISE OPERATION-----------------------------

# blank = np.zeros((400,400),dtype = 'uint8')
# cv.imshow('Blank',blank)
# rectangle = cv.rectangle(blank.copy(),(30,30),(370,370),255,-1) 
# circle = cv.circle(blank.copy(),(200,200),200,255,-1) # (200,200)centre of circle, 200 -> radius, 255->whilte color, -1-> fill the circle by white color
# bitwise_and = cv.bitwise_and(rectangle,circle)
# bitwise_or = cv.bitwise_or(rectangle,circle)
# bitwise_xor = cv.bitwise_xor(rectangle,circle)
# bitwise_not = cv.bitwise_not(rectangle,circle)
# cv.imshow('Bitwise_or',bitwise_or)
# cv.imshow('Bitwise_and',bitwise_and)
# cv.imshow('Bitwise Xor',bitwise_xor)
# cv.imshow('Bitwise_not',bitwise_not)
# # cv.imshow('Rectangle',rectangle)
# # cv.imshow('Circle',circle)
# cv.waitKey(0)
# cv.destroyAllWindows()

# MASKING-------------------------

blank = np.zeros(resized_img.shape[:2],dtype='uint8')
mask=cv.circle(blank,(resized_img.shape[1]//2,resized_img.shape[0]//2),150,255,-1)
masked = cv.bitwise_and(resized_img,resized_img,mask =mask)
cv.imshow('Masked Image',masked)
cv.imshow('Blank image',blank)
cv.waitKey(0)

