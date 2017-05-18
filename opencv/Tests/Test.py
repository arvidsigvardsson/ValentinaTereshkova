import cv2
import numpy as np
import urllib
from clickEvent import pointFinder


pointfinder = pointFinder()
(x1,y1), (x2, y2) = pointfinder.findPoints('test.jpg')


# def click_event(event, x, y, flags, param):
#     global refPt
#     if event == cv2.EVENT_LBUTTONDOWN:
#         print('hello')
#         refPt.append((x,y))
#
#     #elif event == cv2.EVENT_LBUTTONUP:
#     #    print('hello1')
#     #    refPt.append((x, y))
#
#     print(refPt)
#
#
# image = cv2.imread('test.jpg', 1)
# cv2.namedWindow('window')
#
# cv2.setMouseCallback('window', click_event)
#
# clicks = 0
#
# refPt = []
#
#
# #while clicks < 3:
# cv2.imshow('window',image)
# key = cv2.waitKey(1) & 0xFF
#
#     #print(refPt[0])
#     #print(refPt[1])
#
# # if key == ord("c"):
# #      break
#
#
# if cv2.waitKey(0):
#     cv2.destroyAllWindows()
