import numpy as np
import cv2
import imutils

xlist = []
ylist = []

class FindEdge:

    def __init__(self, colorLower, colorUpper):
        self.colorLower = colorLower
        self.colorUpper = colorUpper
        #self.frame = frame


    def get_edges(self, frame):

        hsv = cv2.cvtColor(frame, cv2.COLOR_RGB2HSV)
        mask = cv2.inRange(hsv, self.colorLower, self.colorUpper)
        mask = cv2.erode(mask, None, iterations=1)
        mask = cv2.dilate(mask, None, iterations=2)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, None)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, None)
        cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]

        for c in cnts:
            M = cv2.moments(c)
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
            xlist.append(str(cX))
            ylist.append(str(cY))
            cv2.drawContours(frame, [c], -1, (0, 255, 0), 2)
            cv2.circle(frame, (cX, cY), 7, (255, 255, 255), -1)
            cv2.putText(frame, "center", (cX - 20, cY - 20),
            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)


        cv2.imshow("frame", frame)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        return xlist, ylist





# redLower = (0, 90, 100)
# redUpper = (30, 255, 255)
#
# xlist = []
# ylist = []
#
# frame = cv2.imread('findCorners.jpg')
#
# kernel = np.ones((5,5), np.uint8)
# hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
# mask = cv2.inRange(hsv, redLower, redUpper)
# mask = cv2.erode(mask, None, iterations=1)
# mask = cv2.dilate(mask, None, iterations=2)
# mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, None)
# mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, None)
# cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
#
#
# cnts = cnts[0] if imutils.is_cv2() else cnts[1]
#
# for c in cnts:
#     M = cv2.moments(c)
#     cX = int(M["m10"] / M["m00"])
#     cY = int(M["m01"] / M["m00"])
#     xlist.append(str(cX))
#     ylist.append(str(cY))
#     cv2.drawContours(frame, [c], -1, (0, 255, 0), 2)
#     cv2.circle(frame, (cX, cY), 7, (255, 255, 255), -1)
#     cv2.putText(frame, "center", (cX - 20, cY - 20),
# 		cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
#     cv2.imshow("frame", frame)
#     cv2.imshow("mask", mask)
#     cv2.waitKey(0)
#     cv2.destroyAllWindows()
#
# print(xlist)
# print(ylist)
