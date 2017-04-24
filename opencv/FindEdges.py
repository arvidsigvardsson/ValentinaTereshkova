import numpy as np
import cv2
import imutils

greenLower = (150, 100, 100)
greenUpper = (180, 255, 255)

xlist = []
ylist = []

image = cv2.imread('hejhej1.jpg')

kernel = np.ones((5,5), np.uint8)
hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
mask = cv2.inRange(hsv, greenLower, greenUpper)
mask = cv2.erode(mask, None, iterations=2)
mask = cv2.dilate(mask, None, iterations=2)
mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, None)
mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, None)
cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)


cnts = cnts[0] if imutils.is_cv2() else cnts[1]

for c in cnts:
    M = cv2.moments(c)
    cX = int(M["m10"] / M["m00"])
    cY = int(M["m01"] / M["m00"])
    xlist.append(str(cX))
    ylist.append(str(cY))
    cv2.drawContours(image, [c], -1, (0, 255, 0), 2)
    cv2.circle(image, (cX, cY), 7, (255, 255, 255), -1)
    cv2.putText(image, "center", (cX - 20, cY - 20),
		cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
    cv2.imshow("image", image)
    cv2.imshow("mask", mask)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


print(xlist)
print(ylist)
