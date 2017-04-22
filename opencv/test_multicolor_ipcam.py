import cv2
import urllib
import imutils
import numpy as np
from collections import deque

#from urllib import urlencode
#from urlrequest import Request, urlopen
from threading import Thread
import json
from decorators import async
import requests

@async
def send_async_request(url, payload):
    r = requests.get(url)
    r = requests.get(url, params = payload)
    r = requests.post(url, data = json.dumps(payload))

def send_request(url, payload):
    # url = 'http://192.168.20.133:5000/todo/api/v1.0/coordinates'
    # payload = {'x' : 1200, 'y' : 1300}
    send_async_request(url, payload)



url = 'http://192.168.20.133:5000/todo/api/v1.0/coordinates'


stream=urllib.urlopen('http://192.168.20.149/axis-cgi/mjpg/video.cgi')
bytes=''
pts_red = deque(maxlen = 64)
pts_blue = deque(maxlen = 64)
counter = 0
while(1):
    counter = counter + 1
    bytes+=stream.read(1024)
    a = bytes.find('\xff\xd8')
    b = bytes.find('\xff\xd9')
    if a!=-1 and b!=-1:
        jpg = bytes[a:b+2]
        bytes= bytes[b+2:]
        frame = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8),cv2.IMREAD_COLOR)
    #_,frame = stream.read()
    else:
        continue
    #frame = imutils.resize(frame, width=600)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # lower mask (0-10)
    lower_red = np.array([105,100,100])
    upper_red = np.array([135,255,255])

    lower_blue = np.array([105,100,100])
    upper_blue = np.array([135,255,255])

    kernal=np.ones((5,5), np.uint8)

    red = cv2.inRange(hsv, lower_red, upper_red)
    red = cv2.erode(red, None, iterations=2)
    red = cv2.dilate(red, None, iterations=2)

    blue = cv2.inRange(hsv, lower_blue, upper_blue)
    blue = cv2.erode(blue, None, iterations=2)
    blue = cv2.dilate(blue, None, iterations=2)
    cX = ''
    cY = ''



    res = cv2.bitwise_and(frame, frame, mask=red)
    res1 = cv2.bitwise_and(frame, frame, mask=blue)

    # find contours in the mask and initialize the current
    # (x, y) center of the ball
    cnts_red = cv2.findContours(red.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[-2]
    center_red = None

    cnts_blue = cv2.findContours(blue.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[-2]
    center_blue = None

    if len(cnts_red) > 0:
        # find the largest contour in the mask, then use
        # it to compute the minimum enclosing circle and
        # centroid
        c_red = max(cnts_red, key=cv2.contourArea)
        ((x_red, y_red), radius_red) = cv2.minEnclosingCircle(c_red)
        M_red = cv2.moments(c_red)
        center_red = (int(M_red["m10"] / M_red["m00"]), int(M_red["m01"] / M_red["m00"]))
        cX = center_red[0]
        cY = center_red[1]

        if (counter > 500):
            post_fields = { 'x' : cX , 'y' : cY}
            send_request(url,post_fields)

            counter = 0

        # only proceed if the radius meets a minimum size
        if radius_red > 10:
            # draw the circle and centroid on the frame,
            # then update the list of tracked points
            #cv2.circle(frame, (int(x_red), int(y_red)), int(radius_red),(0, 255, 255), 2)
            cv2.circle(frame, center_red, 3, (30,200, 255), -1)
            cv2.putText(frame,"RED_CENTER", (center_red[0]+10,center_red[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.4,(30, 200, 255),1)
            cv2.putText(frame,"("+str(center_red[0])+","+str(center_red[1])+")", (center_red[0]+10,center_red[1]+15), cv2.FONT_HERSHEY_SIMPLEX, 0.4,(30, 200, 255),1)
    pts_red.appendleft(center_red)

    for i in xrange(1, len(pts_red)):

        if pts_red[i-1] is None or pts_red[i] is None:
            continue

            thickness = int(np.sqrt(args["buffer"] / float(i + 1)) * 2.5)
            cv2.line(frame, pts_red[i - 1], pts_red[i], (0, 0, 255), thickness)

    if len(cnts_blue) > 0:
        # find the largest contour in the mask, then use
        # it to compute the minimum enclosing circle and
        # centroid
        c_blue = max(cnts_blue, key=cv2.contourArea)
        ((x_blue, y_blue), radius_blue) = cv2.minEnclosingCircle(c_blue)
        M_blue = cv2.moments(c_blue)
        center_blue = (int(M_blue["m10"] / M_blue["m00"]), int(M_blue["m01"] / M_blue["m00"]))

        # only proceed if the radius meets a minimum size
        if radius_blue > 10:
            # draw the circle and centroid on the frame,
            # then update the list of tracked points
            #cv2.circle(frame, (int(x_blue), int(y_blue)), int(radius_blue),(0, 255, 255), 2)
            cv2.circle(frame, center_blue, 3, (255, 0, 255), -1)
            cv2.putText(frame,"BLUE_CENTER", (center_blue[0]+10,center_blue[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.4,(255, 0, 255),1)
            cv2.putText(frame,"("+str(center_blue[0])+","+str(center_blue[1])+")", (center_blue[0]+10,center_blue[1]+15), cv2.FONT_HERSHEY_SIMPLEX, 0.4,(255, 0, 255),1)

    pts_blue.appendleft(center_blue)

    for i in xrange(1, len(pts_blue)):

        if pts_blue[i-1] is None or pts_blue[i] is None:
            continue

            thickness = int(np.sqrt(args["buffer"] / float(i + 1)) * 2.5)
            cv2.line(frame, pts_blue[i - 1], pts_blue[i], (0, 0, 255), thickness)




    # request = requests(url, urlencode(post_fields).encode())
    # json = urlopen(request).read().decode()
    # print(json)



    cv2.imshow('frame', frame)
    cv2.imshow('red', red)
    #cv2.imshow('res', res)
    #cv2.imshow('blue', blue)
    #cv2.imshow('res1', res1)
    k = cv2.waitKey(5) & 0xFF
    if k==27:
        break



print center_blue
print center_red
cv2.destroyAllWindows()
