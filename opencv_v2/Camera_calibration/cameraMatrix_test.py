"""
Author: Mikael

Script reads file named court_pic1.jpg
searches the image for four red corners and draws lines between them and displays the image
then undistorts the image with the cameraMatrix and distCoefs from calibration.py
displays the new image and finds the corners and draw new lines between them
in order to show the effect of the undistort method.

"""

import numpy as np
import cv2
import calibration
from FindEdges1 import FindEdge
redLower = (118, 90, 100)
redUpper = (127, 255, 255)
findEdge = FindEdge(redLower, redUpper)

img = cv2.imread( './court_pic1.jpg')
#get coordinates for corners in image
x1list,y1list = findEdge.get_edges(img)
print ('-------------Bild 1 koordinater----------------')
for index in range(0,len(x1list)):
    print(x1list[index], y1list[index])
print ('-----------------------------------------------')
newimage = img.copy()

edge = 0
#draw lines between identified corners
while edge <3:
    cv2.line(newimage, (int(x1list[edge]),int(y1list[edge])), (int(x1list[edge+1]),int(y1list[edge+1])), (255,0,0),1)
    edge += 1
cv2.line(newimage, (int(x1list[0]),int(y1list[0])), (int(x1list[3]),int(y1list[3])), (255,0,0),1)
cv2.imshow('orginal bild', newimage)


cameraMatrix = calibration.camera_matrix
distCoefs = calibration.dist_coeffs
h,  w = newimage.shape[:2]
print("H W",h,w)
newcameramtx, roi = cv2.getOptimalNewCameraMatrix(cameraMatrix, distCoefs, (w, h), 1, (w, h))
print("NEW camera matrix:\n", newcameramtx)
#undistort image
dst = cv2.undistort(img, cameraMatrix, distCoefs, None, newcameramtx)
#get coordinates for corners in new image
x2list,y2list = findEdge.get_edges(dst)
print ('---------------Bild 2 koordinater--------------')
for index in range(0,len(x2list)):
    print(x2list[index], y2list[index])
print ('-----------------------------------------------')
newDst = dst.copy()
edgeDst = 0
#draw lines between corners in image
while edgeDst <3:
    cv2.line(newDst, (int(x2list[edgeDst]),int(y2list[edgeDst])), (int(x2list[edgeDst+1]),int(y2list[edgeDst+1])), (255,0,0),1)
    edgeDst += 1
cv2.line(newDst, (int(x2list[0]),int(y2list[0])), (int(x2list[3]),int(y2list[3])), (255,0,0),1)

cv2.imshow('ny Bild', newDst)
if cv2.waitKey(0):
    cv2.destroyAllWindows
