import cv2
import urllib
import imutils
import numpy as np
from collections import deque
from coordmapping import Mapper
from threading import Thread
from post_request import send_request



url = 'http://192.168.20.145:5000/srv/coordinates'


stream=urllib.urlopen('http://192.168.20.149/axis-cgi/mjpg/video.cgi')
frameCount = 1
bytes=''
mapper = Mapper((180, 461), (634,434), (603,84), (172, 107), 500, 400)


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
    lower_red = np.array([150,100,100])
    upper_red = np.array([180,255,255])

    lower_blue = np.array([105,100,100])
    upper_blue = np.array([130,255,255])

    kernel=np.ones((5,5), np.uint8) # Not used

    red = cv2.inRange(hsv, lower_red, upper_red)
    red = cv2.erode(red, None, iterations=1)
    red = cv2.dilate(red, None , iterations=2)

    blue = cv2.inRange(hsv, lower_blue, upper_blue)
    blue = cv2.erode(blue, None, iterations=2)
    blue = cv2.dilate(blue, None, iterations=2)
    #opening = cv2.morphologyEx(blue, cv2.MORPH_OPEN, kernel)
    #closing = cv2.morphologyEx(opening, cv2.MORPH_OPEN, kernel)

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
        center_red = (int(M_red["m10"] / M_red["m00"]), int(M_red["m01"] / M_red["m00"]))
        crX = center_red[0]
        crY = center_red[1]
        (newcrX, newcrY) = mapper.get_mapped((crX, crY))

        # only proceed if the radius meets a minimum size
        if radius_red > 8:
            # draw the circle and centroid on the frame,
            # then update the list of tracked points
            #cv2.circle(frame, (int(x_red), int(y_red)), int(radius_red),(0, 255, 255), 2)
            cv2.circle(frame, center_red, 3, (30,200, 255), -1)
            cv2.putText(frame,"RED_CENTER", (center_red[0]+10,center_red[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.4,(30, 200, 255),1)
            cv2.putText(frame,"("+str(center_red[0])+","+str(center_red[1])+")", (center_red[0]+10,center_red[1]+15), cv2.FONT_HERSHEY_SIMPLEX, 0.4,(30, 200, 255),1)

    if len(cnts_blue) > 0:
        # find the largest contour in the mask, then use
        # it to compute the minimum enclosing circle and
        # centroid
        c_blue = max(cnts_blue, key=cv2.contourArea)
        ((x_blue, y_blue), radius_blue) = cv2.minEnclosingCircle(c_blue)
        M_blue = cv2.moments(c_blue)
        center_blue = (int(M_blue["m10"] / M_blue["m00"]), int(M_blue["m01"] / M_blue["m00"]))
        cbX = center_blue[0]
        cbY = center_blue[1]
        (newcbX, newcbY) = mapper.get_mapped((cbX, cbY))

        # only proceed if the radius meets a minimum size
        if radius_blue > 8:
            # draw the circle and centroid on the frame,
            # then update the list of tracked points
            #cv2.circle(frame, (int(x_blue), int(y_blue)), int(radius_blue),(0, 255, 255), 2)
            cv2.circle(frame, center_blue, 3, (255, 0, 255), -1)
            cv2.putText(frame,"BLUE_CENTER", (center_blue[0]+10,center_blue[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.4,(255, 0, 255),1)
            cv2.putText(frame,"("+str(center_blue[0])+","+str(center_blue[1])+")", (center_blue[0]+10,center_blue[1]+15), cv2.FONT_HERSHEY_SIMPLEX, 0.4,(255, 0, 255),1)

            if (frameCount > 50):
                post_fields = { 'x' : int(newcbX) , 'y' : int(newcbY)}
                send_request(url, post_fields)
                print('Post request send succesfully!')

                # Uncomment to send coordinates for red_center aswell
                #post_fields = { 'x' : crX, 'y' : crY}
                #send_request(url,post_fields)

                frameCount = 1



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
