import cv2 as cv
import numpy as np

# Rescaling the video and image

def rescaleFrame(frame, scale = 0.2):
    width = int(frame.shape[1] *scale)
    height = int(frame.shape[0] *scale)
    dimensions= (width,height)
    return cv.resize(frame, dimensions, interpolation=cv.INTER_AREA)

# Reading the Image ----------

# image = cv.imread('/home/yogendra/Documents/AIEngineer/OpenCV/manja-vitolic-gKXKBY-C-Dk-unsplash.jpg')
# resized_image = rescaleFrame(image)
# cv.imshow('Original Image',image)
# cv.imshow('Resized Image', resized_image)
# cv.waitKey(0)
# cv.destroyAllWindows()

# Reading the Video ---------

# video = cv.VideoCapture("/home/yogendra/Documents/AIEngineer/OpenCV/19607907-hd_1920_1080_30fps.mp4")
# while True:
#     isTrue, frame = video.read()
#     resized_video = rescaleFrame(frame)
#     cv.imshow('Original Video', frame)
#     cv.imshow('Video', resized_video)
#     if cv.waitKey(20) & 0xFF == ord('d'):
#         break   
# video.release()
# cv.destroyAllWindows()

# Make a blank image and draw line,circle,rectangle and also write some text on blank image. ------------

# Blank = np.zeros((500,500,3),dtype = 'uint8')

# Blank[:] = 255,0,0   # Give the color to the blank image(BLUE colour)
# cv.circle(Blank, (250,250), 100, (0,255,0), thickness=2)
# cv.imshow('Blank', Blank)
# cv.line(Blank,(250,250),(350,250),(0,0,255),thickness = 3)
# cv.imshow('Blank',Blank)
# cv.putText(Blank,"Hello sudha kaisi ho?",(23,23),cv.FONT_HERSHEY_TRIPLEX,1,(0,255,255),2) # Write text on image
# cv.imshow('Text',Blank)
# cv.waitKey(0)

# Apply some functions on image ----------------

img = cv.imread('/home/yogendra/Documents/AIEngineer/OpenCV/manja-vitolic-gKXKBY-C-Dk-unsplash.jpg')
img1 = rescaleFrame(img)
# cv.imshow('Real Image',img1)
# gray = cv.cvtColor(img1,cv.COLOR_BGR2GRAY)   # Convert the image RGB to GRAY
# cv.imshow('Gray',gray)
# blur = cv.GaussianBlur(img1,(3,3),cv.BORDER_DEFAULT) # Convert the  image to BLUR
# cv.imshow('Blur',blur)
# canny = cv.Canny(img1,100,100) # Convert the image into edges
# cv.imshow('Canny',canny)
# cropped = img[100:322,109:499]
# cv.imshow('Cropped',cropped)  # Use to crop the image
# cv.waitKey(0)

# Translation -----------------
# X  ->Right, -X ->Left, y -> Down, -y -> UP

# def translate(img,x,y):
#     transMat = np.float32([[1,0,x],[0,1,y]])
#     dimension = (img1.shape[1],img1.shape[0])    # (width,height)
#     return cv.warpAffine(img1,transMat,dimension)
# translated_image = translate(img1,100,69)
# cv.imshow('Translate',translated_image)

# Rotation --------------------
# def Rotations(img,angle,rotPoint = None):
#     (height,width) = img.shape[:2]
#     if rotPoint is None:
#         rotPoint = (width//2,height//2)
#     rotMat = cv.getRotationMatrix2D(rotPoint,angle,1.0)
#     dimensions = (width,height)
#     return cv.warpAffine(img1, rotMat,dimensions)
# rotated = Rotations(img1,-45)
# cv.imshow('Rotated',rotated)
# cv.waitKey(0)

# Flipping ----------------------------
# flip1 = cv.flip(img1,0)
# flip2 = cv.flip(img1,1)
# flip3 = cv.flip(img1,-1)
# cv.imshow('Flip1',flip1)
# cv.imshow('Flip2',flip2)
# cv.imshow('Flip3',flip3)
# cv.waitKey(0)

# Contours Indentification ---------------------
cany = cv.Canny(img1,109,150) # these numbers are pixels, if pixels is less than 125 then don't consider as edge and if the pixels is above 175 and then consider as edge
# cv.imshow('Canny',cany)
gray = cv.cvtColor(img1,cv.COLOR_BGR2GRAY)
# cv.imshow('Gray',gray)
ret,thresh = cv.threshold(img1,109,150,cv.THRESH_BINARY) # if pixels below 109 then it will be zero(black) and if the pixels are bigger 150 then it will be white,if the pixels are between 109 and 150 then it will wil check if the pixels is connected with edge then will coung as black otherwise white.
cv.imshow('Thresh',thresh)
blank = np.zeros(img1.shape,dtype = 'uint8')
# cv.imshow('Blank',blank)
contours1,hierarchies1 = cv.findContours(cany,cv.RETR_CCOMP,cv.CHAIN_APPROX_SIMPLE)
contours2,hierarchies2 = cv.findContours(gray,cv.RETR_CCOMP,cv.CHAIN_APPROX_SIMPLE)
cv.drawContours(blank,contours1,-1,(0,0,255),2)
cv.imshow('Contours Draws',blank)
cv.waitKey(0)
print(f'{len(contours1)}contours found!')
print(f'{len(contours2)}contours found!')
    
