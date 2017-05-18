import urllib
import cv2
import numpy as np
import imutils
import time as t
class IpCamera:



    def __init__(self):
        self = self

    def getFrame(self):
        stream=urllib.urlopen('http://192.168.20.149/axis-cgi/mjpg/video.cgi')
        bytes=''
        while (1):
            bytes+=stream.read(1024)
            a = bytes.find('\xff\xd8')
            b = bytes.find('\xff\xd9')
            if a!=-1 and b!=-1:
                jpg = bytes[a:b+2]
                bytes= bytes[b+2:]
                frame = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8),cv2.IMREAD_COLOR)
                return frame
