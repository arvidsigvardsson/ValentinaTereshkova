from collections import deque
import numpy as np
import argparse
import imutils
import cv2
import urllib
from FindEdges import FindEdge
from ipcamera import IpCamera

xlist = []
ylist = []

# ap = argparse.ArgumentParser()
# args = vars(ap.parse_args())
#
#
# redLower = (150, 90, 100)
# redUpper = (180, 255, 255)

# if not args.get("video", False):
#     camera = cv2.VideoCapture(0)
# else:
#     camera = cv2.VideoCapture(args["video"])
#
# (grabbed, frame) = camera.read()

# frame = cv2.imread('findCorners.jpg')
#
# findEdge = FindEdge(redLower, redUpper)
#
# xlist, ylist = findEdge.get_edges(frame)
#
# print(xlist, ylist)
