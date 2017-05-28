import cv2
import urllib
import imutils
import numpy as np
import time
from collections import deque
from coordmapping import Mapper
from post_request import send_request
from FindEdges1 import FindEdge
from clickEvent import pointFinder
from IpCamera import IpCam



roihalfsize = 12


url = 'http://192.168.20.100:5000/srv/coordinates'
#stream=urllib.urlopen('http://192.168.20.149/axis-cgi/mjpg/video.cgi')

cameraUrl = 'http://192.168.20.149/axis-cgi/mjpg/video.cgi'


initPosition = 1
frameCount = 1
bytes=''
lower_blue = np.array([90,80,100])
upper_blue = np.array([160,255,255])
#redLower = (118, 90, 100)
#redUpper = (127, 255, 255)
#findEdge = FindEdge(redLower, redUpper)
#frame = cv2.imread('.\calibration.jpg', 1)

#xlist,ylist = findEdge.get_edges(frame)

pointfinder = pointFinder()
#get points for two diodes and corners
#Klick order:
#1: Diode 2:Diode 3: 1st Corner  4: 2nd Corner 5: 3d Corner 6: 4th Corner
ipcam = cv2.VideoCapture(0)
_,frame = ipcam.read()
pList = pointfinder.findPoints(frame)
(x1, y1) = pList[0]
(x2, y2) = pList[1]
#ipcam = IpCam(cameraUrl)
#ipcam.start()





#for c in xlist:
#    print (str(c)+'xhorn')
#for c in ylist:
#    print (str(c)+'yhorn')




#mapper = Mapper((xlist[0], ylist[0]), (xlist[1],ylist[1]), (xlist[2],ylist[2]), (xlist[3], ylist[3]), 500.0, 400.0, (278.9, 134.6, 801.0))
mapper = Mapper(pList[2], pList[3], pList[4], pList[5], 500.0, 400.0, (278.9, 134.6, 801.0))
while(frameCount):

    _,frame = ipcam.read()

    if frame == None:
        continue


    shading_led1 = np.zeros((frame.shape[0], frame.shape[1], 3), np.uint8)
    shading_led2 = np.zeros((frame.shape[0], frame.shape[1], 3), np.uint8)
    gray_led1 = cv2.cvtColor(shading_led1, cv2.COLOR_BGR2GRAY)  #---converting to gray
    gray_led2 = cv2.cvtColor(shading_led2, cv2.COLOR_BGR2GRAY)  #---converting to gray
    if initPosition == 1:
        roi1 = cv2.rectangle(gray_led1, (int(x1) - roihalfsize, int(y1) - roihalfsize), (int(x1) + roihalfsize, int(y1) + roihalfsize), (255, 255, 255), -1)
        roi2 = cv2.rectangle(gray_led2, (int(x2) - roihalfsize, int(y2) - roihalfsize), (int(x2) + roihalfsize, int(y2) + roihalfsize), (255, 255, 255), -1)
        initPosition = 0


    frame1 = cv2.bitwise_and(frame, frame, mask = roi1)
    frame2 = cv2.bitwise_and(frame, frame, mask = roi2)

    #if (roi2 != ''):
    #    frame2 = cv2.bitwise_and(frame,frame,mask = roi)

    hsv_blue1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2HSV)
    hsv_blue2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2HSV)




    kernel=np.ones((2,2), np.uint8) # Not used

    blue1 = cv2.inRange(hsv_blue1, lower_blue, upper_blue)
    blue1 = cv2.erode(blue1, kernel, iterations=2)
    blue1 = cv2.dilate(blue1, kernel, iterations=3)

    blue2 = cv2.inRange(hsv_blue2, lower_blue, upper_blue)
    blue2 = cv2.erode(blue2, kernel, iterations=2)
    blue2 = cv2.dilate(blue2, kernel, iterations=3)
    #opening = cv2.morphologyEx(blue, cv2.MORPH_OPEN, kernel)
    #closing = cv2.morphologyEx(opening, cv2.MORPH_OPEN, kernel)

    # res1 = cv2.bitwise_and(frame, frame, mask=blue)
    # res = cv2.bitwise_and(frame, frame, mask=red)
    cnts_blue1 = cv2.findContours(blue1.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[-2]
    center_blue1 = None

    cnts_blue2 = cv2.findContours(blue2.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[-2]
    center_blue2 = None


    if len(cnts_blue1) > 0:
        # find the largest contour in the mask, then use
        # it to compute the minimum enclosing circle and
        # centroid
        c_blue = max(cnts_blue1, key=cv2.contourArea)
        ((x_blue, y_blue), radius_blue) = cv2.minEnclosingCircle(c_blue)
        M_blue = cv2.moments(c_blue)
        if M_blue["m00"] != 0:
            center_blue1 = (float(M_blue["m10"] / M_blue["m00"]), float(M_blue["m01"] / M_blue["m00"]))
            cbX1 = center_blue1[0]
            cbY1 = center_blue1[1]
            roi1 = cv2.rectangle(shading_led1, (int(cbX1) - roihalfsize, int(cbY1) - roihalfsize), (int(cbX1) + roihalfsize, int(cbY1) + roihalfsize),(255, 255, 255), -1)
            roi1 = cv2.cvtColor(roi1,cv2.COLOR_BGR2GRAY)
            (newcbX1, newcbY1) = mapper.get_mapped_with_height((cbX1, cbY1), 28.5)
            #(newcbX, newcbY) = mapper.get_mapped((cbX, cbY))


        # only proceed if the radius meets a minimum size
        if radius_blue > 5:
            # draw the circle and centroid on the frame,
            # then update the list of tracked points
            #cv2.circle(frame, (int(x_blue), int(y_blue)), int(radius_blue),(0, 255, 255), 2)
            cv2.circle(frame1, (int(center_blue1[0]), int(center_blue1[1])), 3, (255, 0, 255), -1)
            cv2.putText(frame1,"BLUE_CENTER1", (int(center_blue1[0]) + 10, int(center_blue1[1])), cv2.FONT_HERSHEY_SIMPLEX, 0.4,(255, 0, 255),1)
            cv2.putText(frame1,"("+str(int(center_blue1[0]))+","+str(int(center_blue1[1]))+")", (int(center_blue1[0]) + 10, int(center_blue1[1]) + 15), cv2.FONT_HERSHEY_SIMPLEX, 0.4,(255, 0, 255),1)


    if len(cnts_blue2) > 0:
        # find the largest contour in the mask, then use
        # it to compute the minimum enclosing circle and
        # centroid
        c_blue = max(cnts_blue2, key=cv2.contourArea)
        ((x_blue, y_blue), radius_blue) = cv2.minEnclosingCircle(c_blue)
        M_blue = cv2.moments(c_blue)
        if M_blue["m00"] != 0:
            center_blue2 = (float(M_blue["m10"] / M_blue["m00"]), float(M_blue["m01"] / M_blue["m00"]))
            cbX2 = center_blue2[0]
            cbY2 = center_blue2[1]
            roi2 = cv2.rectangle(shading_led2, (int(cbX2) - roihalfsize, int(cbY2) - roihalfsize),(int(cbX2) + roihalfsize, int(cbY2) + roihalfsize), (255, 255, 255), -1)
            roi2 = cv2.cvtColor(roi2, cv2.COLOR_BGR2GRAY)
            (newcbX2, newcbY2) = mapper.get_mapped_with_height((cbX2, cbY2), 28.5)
            #(newcbX, newcbY) = mapper.get_mapped((cbX, cbY))


        # only proceed if the radius meets a minimum size
        if radius_blue > 7:
            # draw the circle and centroid on the frame,
            # then update the list of tracked points
            #cv2.circle(frame, (int(x_blue), int(y_blue)), int(radius_blue),(0, 255, 255), 2)
            cv2.circle(frame2, (int(center_blue2[0]), int(center_blue2[1])), 3, (255, 0, 255), -1)
            cv2.putText(frame2,"BLUE_CENTER2", (int(center_blue2[0]) + 10, int(center_blue2[1])), cv2.FONT_HERSHEY_SIMPLEX, 0.4,(255, 0, 255),1)
            cv2.putText(frame2,"("+str(int(center_blue2[0]))+","+str(int(center_blue2[1]))+")", (int(center_blue2[0]) + 10, int(center_blue2[1]) + 15), cv2.FONT_HERSHEY_SIMPLEX, 0.4,(255, 0, 255),1)

            if (frameCount > 9):
                # print('----------LED1 Coordinates-------------')
                # print(int(cbX1))
                # print(int(cbY1))
                # print('----------LED2 Coordinates-------------')
                # print(int(cbX2))
                # print(int(cbY2))
                #post_fields = { 'x1' : int(cbX1) , 'y1' : int(cbY1), 'x2' : int(cbX2), 'y2' : int(cbY2)} #Only blue center coordinates
                # send_request(url, post_fields)
                print('Post request send succesfully!')

                # Uncomment to send coordinates for red_center aswell
                #post_fields = { 'x1' : int(newcbX), 'y1' : int(newcbY), 'x2' : int(newcrX), 'y2' : int(newcrY) }
                #send_request(url,post_fields)

                frameCount = 1


    #endTime = int(round(time.time() * 1000))
    #oneFrame = endTime - startTime
    #print('One frame time:' + str(oneFrame))
    #cv2.imshow('frame', frame)
    cv2.imshow('frame1', frame1)
    cv2.imshow('frame2', frame2)
    cv2.imshow('blue1', blue1)
    cv2.imshow('blue2', blue2)
    frameCount += 1
    #cv2.imshow('res', res)
    #cv2.imshow('blue', blue)
    #cv2.imshow('res1', res1)
    k = cv2.waitKey(5) & 0xFF
    if k==27:
        cv2.destroyAllWindows()
        #ipcam.shut_down()
        break
