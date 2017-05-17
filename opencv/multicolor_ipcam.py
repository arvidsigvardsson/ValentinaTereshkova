import cv2
import urllib
import imutils
import numpy as np
import time
from collections import deque
from coordmapping import Mapper, compensate_for_measured_error
from threading import Thread
from post_request import send_request
from FindEdges import FindEdge

xlist = []
ylist = []

bytes=''
url = 'http://192.168.20.57:5000/srv/coordinates'
stream=urllib.urlopen('http://192.168.20.149/axis-cgi/mjpg/video.cgi')
#frame = cv2.imread('hejhej1.jpg')



#redLower = (115, 90, 100)
#redUpper = (128, 255, 255)
#findEdge = FindEdge(redLower, redUpper)
#xlist,ylist = findEdge.get_edges(frame)


frameCount = 1
mapper = Mapper((168.2, 475.7), (633.5,466.8), (619.7,87.5), (156.1, 111.2), 500.0, 400.0, (304.4, 189.3, 801.0))

while(frameCount):
    bytes+=stream.read(1024)
    a = bytes.find('\xff\xd8')
    b = bytes.find('\xff\xd9')
    if a!=-1 and b!=-1:
        jpg = bytes[a:b+2]
        bytes= bytes[b+2:]
        frame = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8),cv2.IMREAD_COLOR)
    else:
        continue
    #frame = imutils.resize(frame, width=600)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # lower mask (0-10)
    lower_red = np.array([0,100,100])
    upper_red = np.array([30,255,255])

    lower_blue = np.array([110,100,100])
    upper_blue = np.array([130,255,255])

    kernel=np.ones((2,2), np.uint8) # Not used

    red = cv2.inRange(hsv, lower_red, upper_red)
    red = cv2.erode(red, None, iterations=1)
    red = cv2.dilate(red, None , iterations=3)

    blue = cv2.inRange(hsv, lower_blue, upper_blue)
    blue = cv2.erode(blue, kernel, iterations=1)
    blue = cv2.dilate(blue, kernel, iterations=3)

    #opening = cv2.morphologyEx(blue, cv2.MORPH_OPEN, None)
    #closing = cv2.morphologyEx(opening, cv2.MORPH_OPEN, None)

    # res1 = cv2.bitwise_and(frame, frame, mask=blue)
    # res = cv2.bitwise_and(frame, frame, mask=red)

    cnts_red = cv2.findContours(red.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[-2]
    center_red = None

    cnts_blue = cv2.findContours(blue.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[-2]
    center_blue = None

    if len(cnts_red) > 0:
        c_red = max(cnts_red, key=cv2.contourArea)
        ((x_red, y_red), radius_red) = cv2.minEnclosingCircle(c_red)
        M_red = cv2.moments(c_red)
        center_red = (float(M_red["m10"] / M_red["m00"]), float(M_red["m01"] / M_red["m00"]))
        crX = center_red[0]
        crY = center_red[1]
        (newcrX, newcrY) = mapper.get_mapped_with_height((crX, crY), 10)

        # only proceed if the radius meets a minimum size
        if radius_red > 10:
            # draw the circle and centroid on the frame,
            # then update the list of tracked points
            #cv2.circle(frame, (int(x_red), int(y_red)), int(radius_red),(0, 255, 255), 2)
            cv2.circle(frame, (int(center_red[0]), int(center_red[1])), 3, (30,200, 255), -1)
            cv2.putText(frame,"RED_CENTER", (int(center_red[0]) + 10, int(center_red[1])), cv2.FONT_HERSHEY_SIMPLEX, 0.4,(30, 200, 255),1)
            cv2.putText(frame,"("+str(int(center_red[0]))+","+str(int(center_red[1]))+")", (int(center_red[0]) + 10, int(center_red[1]) + 15), cv2.FONT_HERSHEY_SIMPLEX, 0.4,(30, 200, 255),1)

    if len(cnts_blue) > 0:
        c_blue = max(cnts_blue, key=cv2.contourArea)
        ((x_blue, y_blue), radius_blue) = cv2.minEnclosingCircle(c_blue)
        M_blue = cv2.moments(c_blue)
        if M_blue["m00"] != 0:
            center_blue = (float(M_blue["m10"] / M_blue["m00"]), float(M_blue["m01"] / M_blue["m00"]))
            cbX = center_blue[0]
            cbY = center_blue[1]
            (newcbX1, newcbY1) = mapper.get_mapped_with_height((cbX, cbY), 3.3)
            (newcbX1, newcbY1) = compensate_for_measured_error((newcbX1, newcbY1))
            #(newcbX, newcbY) = mapper.get_mapped_with_height_compensated((cbX, cbY), 28.5)


            #(newcbX, newcbY) = mapper.get_mapped((cbX, cbY))


        # only proceed if the radius meets a minimum size
        if radius_blue > 6:

            #cv2.circle(frame, (int(x_blue), int(y_blue)), int(radius_blue),(0, 255, 255), 2)
            cv2.circle(frame, (int(center_blue[0]), int(center_blue[1])), 3, (255, 0, 255), -1)
            cv2.putText(frame,"BLUE_CENTER", (int(center_blue[0]) + 10, int(center_blue[1])), cv2.FONT_HERSHEY_SIMPLEX, 0.4,(255, 0, 255),1)
            cv2.putText(frame,"("+str(int(center_blue[0]))+","+str(int(center_blue[1]))+")", (int(center_blue[0]) + 10, int(center_blue[1]) + 15), cv2.FONT_HERSHEY_SIMPLEX, 0.4,(255, 0, 255),1)

            if (frameCount > 10):

                post_fields = { 'x1' : int(newcbX1) , 'y1' : int(newcbY1), 'x2' : 0, 'y2' : 0} #Only blue center coordinates
                send_request(url, post_fields)
                print('-------------------OpenCV coordinates------------------')
                print(int(cbX))
                print(int(cbY))
                #print('-------------------Height compensated------------------')
                #print(int(newcbX))
                #print(int(newcbY))
                print('-------------------Height not compensated--------------')
                print(int(newcbX1))
                print(int(newcbY1))
                #print('Post request send succesfully!')

                # Uncomment to send coordinates for red_center aswell
                #post_fields = { 'x1' : int(newcbX), 'y1' : int(newcbY), 'x2' : int(newcrX), 'y2' : int(newcrY) }
                #send_request(url,post_fields)

                frameCount = 1


    #endTime = int(round(time.time() * 1000))
    #oneFrame = endTime - startTime
    #print('One frame time:' + str(oneFrame))
    cv2.imshow('frame', frame)
    cv2.imshow('red', red)
    cv2.imshow('blue', blue)
    frameCount += 1
    #cv2.imshow('res', res)
    #cv2.imshow('blue', blue)
    #cv2.imshow('res1', res1)
    k = cv2.waitKey(5) & 0xFF
    if k==27:
        break
