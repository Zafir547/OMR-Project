import cv2
import numpy as np
import utlis


path = "1.jpg"
widthImg = 700
heightImg = 700



img = cv2.imread(path)

# PREPROCESSING
img = cv2.resize(img, (widthImg, heightImg))
imgCountours = img.copy()
imgGray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
imgBlur = cv2.GaussianBlur(imgGray,(5,5),1)
imgCanny = cv2.Canny(imgBlur,10,50)

# FINDING ALL COUNTOURS
countours, hierarchy = cv2.findContours(imgCanny,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
cv2.drawContours(imgCountours,countours,-1,(0,255,0),10)

# FIND RECTANGLES
utlis.rectCountour(countours)

imgBlank = np.zeros_like(img)
imageArray = ([img,imgGray,imgBlur,imgCanny],
              [imgCountours,imgBlank,imgBlank,imgBlank])

imgStacked = utlis.stackImages(imageArray,0.5)

cv2.imshow("Stacked Images", imgStacked)
cv2.waitKey(0)