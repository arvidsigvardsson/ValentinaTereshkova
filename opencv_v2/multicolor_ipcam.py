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


# Define variables for coordinates of blue LED1 and blue LED2 and the size of the ROI
roihalfsize = 30
newcbX1 = 0
newcbY1 = 0
newcbX2 = 0
newcbY2 = 0

# url for the server so opencv can post coordinates and fetch the mjpeg stream from the camera
url = 'http://192.168.0.3:5000/srv/coordinates'
#cameraUrl = 'http://192.168.20.149/axis-cgi/mjpg/video.cgi'

initPosition = 1 # Variable is used to set the starting position of LED1 and LED2
frameCount = 1   # Controls how often post-request is sent to the server

#Bounds for HSV-scale when filtering the image
lower_blue = np.array([110,80,100])
upper_blue = np.array([130,255,255])


cap = cv2.VideoCapture(0)

#Loads the image to set the starting position for LED1, LED2
pointfinder = pointFinder()
(x1, y1), (x2, y2) = pointfinder.findPoints('test.jpg')

mapper = Mapper((149.0, 465.0), (582.0,445.0), (562.0,93.0), (131.0, 123.0), 500.0, 400.0, (303.9, 188.9, 801.0))
while(frameCount):

    ret, frame = cap.read()
#    frame = ipcam.getFrame()

    #If frame is not defined, continue to next iteration of loop
    if frame == None:
        continue

    # Covers frame1 and frame2 with a blackforegound to filter out the part of the image that's not intresting
    shading_led1 = np.zeros((frame.shape[0], frame.shape[1], 3), np.uint8)
    shading_led2 = np.zeros((frame.shape[0], frame.shape[1], 3), np.uint8)
    gray_led1 = cv2.cvtColor(shading_led1, cv2.COLOR_BGR2GRAY)  #---converting to gray
    gray_led2 = cv2.cvtColor(shading_led2, cv2.COLOR_BGR2GRAY)  #---converting to gray

    #If it's the first iteration, starting position of ROI1, ROI2 are set. Else it will be based on LED1 and LED2 latest position
    if initPosition == 1:
        roi1 = cv2.rectangle(gray_led1, (x1 - roihalfsize, y1 - roihalfsize), (x1 + roihalfsize, y1 + roihalfsize), (255, 255, 255), -1)
        roi2 = cv2.rectangle(gray_led2, (x2 - roihalfsize, y2 - roihalfsize), (x2 + roihalfsize, y2 + roihalfsize), (255, 255, 255), -1)
        initPosition = 0


    #Filtering of the image for the color blue, and then removes noise
    frame1 = cv2.bitwise_and(frame, frame, mask = roi1)
    frame2 = cv2.bitwise_and(frame, frame, mask = roi2)

    hsv_blue1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2HSV)
    hsv_blue2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2HSV)

    kernel=np.ones((2,2), np.uint8) #Sets the size of the kernel used for erode and dilate

    blue1 = cv2.inRange(hsv_blue1, lower_blue, upper_blue)
    blue1 = cv2.erode(blue1, kernel, iterations=2)
    blue1 = cv2.dilate(blue1, kernel, iterations=3)

    blue2 = cv2.inRange(hsv_blue2, lower_blue, upper_blue)
    blue2 = cv2.erode(blue2, kernel, iterations=2)
    blue2 = cv2.dilate(blue2, kernel, iterations=3)

    cnts_blue1 = cv2.findContours(blue1.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[-2]
    center_blue1 = None

    cnts_blue2 = cv2.findContours(blue2.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[-2]
    center_blue2 = None


    #Only proceed if there is any contours in the image
    if len(cnts_blue1) > 0:
        c_blue = max(cnts_blue1, key=cv2.contourArea) #Find the largest contour
        ((x_blue, y_blue), radius_blue) = cv2.minEnclosingCircle(c_blue) # Calculate the minimum enclosing circle
        M_blue = cv2.moments(c_blue) #Calulate the geometrical center of the circle
        if M_blue["m00"] != 0:
            center_blue1 = (float(M_blue["m10"] / M_blue["m00"]), float(M_blue["m01"] / M_blue["m00"])) #Retrives the (x,y) - coordinates for the center
            cbX1 = center_blue1[0]
            cbY1 = center_blue1[1]
            roi1 = cv2.rectangle(shading_led1, (int(cbX1) - roihalfsize, int(cbY1) - roihalfsize), (int(cbX1) + roihalfsize, int(cbY1) + roihalfsize),(255, 255, 255), -1) #Updated the ROI with the LED:s latest coordinates
            roi1 = cv2.cvtColor(roi1,cv2.COLOR_BGR2GRAY)
            #(newcbX1, newcbY1) = mapper.get_mapped_with_height((cbX1, cbY1), 27.5)
            (newcbX1, newcbY1) = mapper.get_mapped_with_height_compensated((cbX1, cbY1), 41)


        # only proceed if the radius meets a minimum size
        if radius_blue > 7:
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
            (newcbX2, newcbY2) = mapper.get_mapped_with_height_compensated((cbX2, cbY2), 41)
            #(newcbX2, newcbY2) = mapper.get_mapped_with_height((cbX2, cbY2), 27.5)


        # only proceed if the radius meets a minimum size
        if radius_blue > 7:
            # draw the circle and centroid on the frame,
            # then update the list of tracked points
            #cv2.circle(frame, (int(x_blue), int(y_blue)), int(radius_blue),(0, 255, 255), 2)
            cv2.circle(frame2, (int(center_blue2[0]), int(center_blue2[1])), 3, (255, 0, 255), -1)
            cv2.putText(frame2,"BLUE_CENTER2", (int(center_blue2[0]) + 10, int(center_blue2[1])), cv2.FONT_HERSHEY_SIMPLEX, 0.4,(255, 0, 255),1)
            cv2.putText(frame2,"("+str(int(center_blue2[0]))+","+str(int(center_blue2[1]))+")", (int(center_blue2[0]) + 10, int(center_blue2[1]) + 15), cv2.FONT_HERSHEY_SIMPLEX, 0.4,(255, 0, 255),1)

    if (frameCount > 9):
        print('----------LED1 Coordinates-------------')
        print(int(newcbX1))
        print(int(newcbY1))
        print('----------LED2 Coordinates-------------')
        print(int(newcbX2))
        print(int(newcbY2))
        post_fields = { 'x1' : int(newcbX1) , 'y1' : int(newcbY1), 'x2' : int(newcbX2), 'y2' : int(newcbY2)} #Only blue center coordinates
        send_request(url, post_fields)
        print('Post request send succesfully!')
        frameCount = 1

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
        #ipcam.shut_down()
        cv2.destroyAllWindows()
        break
