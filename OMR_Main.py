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
imgBiggestContours = img.copy()
imgGray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
imgBlur = cv2.GaussianBlur(imgGray,(5,5),1)
imgCanny = cv2.Canny(imgBlur,10,50)

# FINDING ALL COUNTOURS
countours, hierarchy = cv2.findContours(imgCanny,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
cv2.drawContours(imgCountours,countours,-1,(0,255,0),10)

# FIND RECTANGLES
rectCon = utlis.rectCountour(countours)
biggestContour = utlis.getCornerPoints(rectCon[0])
gradePoints = utlis.getCornerPoints(rectCon[1])
# print(biggestContour)

if biggestContour.size != 0 and gradePoints.size !=0:
    cv2.drawContours(imgBiggestContours,biggestContour,-1,(0,255,0),10)
    cv2.drawContours(imgBiggestContours,gradePoints,-1,(255,0,0),10)

    biggestContour = utlis.reorder(biggestContour)
    gradePoints = utlis.reorder(gradePoints)

    pt1 = np.float32(biggestContour)
    pt2 = np.float32([[0,0],[widthImg,0],[0,heightImg],[widthImg,heightImg]])
    matrix = cv2.getPerspectiveTransform(pt1,pt2)
    imgWarpColored = cv2.warpPerspective(img,matrix,(widthImg,heightImg))

    ptG1 = np.float32(gradePoints)
    ptG2 = np.float32([[0,0],[325,0],[0,150],[325,150]])
    matrixG = cv2.getPerspectiveTransform(ptG1,ptG2)
    imgGradeDisplay = cv2.warpPerspective(img,matrixG,(325,150))
    # cv2.imshow("Grade",imgGradeDisplay)

    # APPLY THRESHOLD
    imgWarpGray = cv2.cvtColor(imgWarpColored,cv2.COLOR_BGR2GRAY)
    imgThresh = cv2.threshold(imgWarpGray,170,255,cv2.THRESH_BINARY_INV)[1]



imgBlank = np.zeros_like(img)
imageArray = ([img,imgGray,imgBlur,imgCanny],
              [imgCountours,imgBiggestContours,imgWarpColored,imgThresh])

imgStacked = utlis.stackImages(imageArray,0.5)

cv2.imshow("Stacked Images", imgStacked)
cv2.waitKey(0)