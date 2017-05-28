#!/usr/bin/env python

'''
Edited by Mikael
camera calibration for distorted images with chess board samples
reads distorted images, calculates the calibration and write undistorted images

usage:
    calibrate.py [--debug <output path>] [--squareSize] [<image mask>]
    Update: script will open URL to defined ipcamera and let user angle portrait between pictures
    picture is taken with spacebar when satisfied with angle, prints out cameraMatrix and distCoefs

default values:
    --debug:    ./output/
    --squareSize: 1.0
    <image mask> defaults to ../data/left*.jpg
'''

# Python 2/3 compatibility
from __future__ import print_function

import numpy as np
import cv2

# local modules
from common import splitfn
import urllib
# built-in modules
import os
import requests
import time


if __name__ == '__main__':
    import sys
    import getopt
    from glob import glob
    counter = 0
    picUrl='http://192.168.20.149/jpg/image.jpg?size=3'
    #while counter <10:
    matrixFile = open("MatrixAndCoefs.txt", "wb")
    #read new frame from ipcam, when space pressed, save picture to designated folder and
    while counter < 10:
        imgData = requests.get(picUrl).content
        frame = cv2.imdecode(np.fromstring(imgData, dtype=np.uint8),cv2.IMREAD_COLOR)
        cv2.imshow('frame', frame)
        k = cv2.waitKey(10) & 0xFF
        if k == 32:
            name = './test/pic'+str(counter)+'.jpg'
            #img_data = requests.get(pic_url).content
            with open(name, 'wb') as handler:
                handler.write(imgData)
                counter += 1
                time.sleep(1)
                print('bild: '+str(counter))


    args, imgMask = getopt.getopt(sys.argv[1:], '', ['debug=', 'squareSize='])
    args = dict(args)
    args.setdefault('--debug', './output/')
    args.setdefault('--squareSize', 1.0)


    if not imgMask:
        imgMask = './test/pic*.jpg'  # default
    else:
        imgMask = imgMask[0]

    imgNames = glob(imgMask)
    debug_dir = args.get('--debug')
    if not os.path.isdir(debug_dir):
        os.mkdir(debug_dir)
    squareSize = float(args.get('--squareSize'))

    patternSize = (7, 7)
    patternPoints = np.zeros((np.prod(patternSize), 3), np.float32)
    patternPoints[:, :2] = np.indices(patternSize).T.reshape(-1, 2)
    patternPoints *= squareSize

    objPoints = []
    imgPoints = []
    h, w = 0, 0
    imgNames_undistort = []
    for fn in imgNames:
        print('processing %s... ' % fn, end='')
        img = cv2.imread(fn, 0)
        if img is None:
            print("Failed to load", fn)
            continue

        h, w = img.shape[:2]
        found, corners = cv2.findChessboardCorners(img, patternSize)
        if found:
            term = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_COUNT, 30, 0.1)
            cv2.cornerSubPix(img, corners, (5, 5), (-1, -1), term)

        if debug_dir:
            vis = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
            cv2.drawChessboardCorners(vis, patternSize, corners, found)
            path, name, ext = splitfn(fn)
            outfile = debug_dir + name + '_chess.png'
            cv2.imwrite(outfile, vis)
            if found:
                imgNames_undistort.append(outfile)

        if not found:
            print('chessboard not found')
            continue

        imgPoints.append(corners.reshape(-1, 2))
        objPoints.append(patternPoints)

        print('ok')


    # calculate camera distortion
    rms, cameraMatrix, distCoefs, rvecs, tvecs = cv2.calibrateCamera(objPoints, imgPoints, (w, h), None, None)
    #print camera matrix and distcoefs
    print("\nRMS:", rms)
    print("camera matrix:\n", cameraMatrix)
    print("distortion coefficients: ", distCoefs)

    # undistort the image with the calibration
    print('')
    for img_found in imgNames_undistort:
        img = cv2.imread(img_found)

        h,  w = img.shape[:2]
        print("H W",h,w)
        newcameramtx, roi = cv2.getOptimalNewCameraMatrix(cameraMatrix, distCoefs, (w, h), 1, (w, h))
        print("NEW camera matrix:\n", newcameramtx)
        dst = cv2.undistort(img, cameraMatrix, distCoefs, None, newcameramtx)

        # crop and save the image
        x, y, w, h = roi
        x1,y1,w1,h1 = (x, y, w, h)

        dst = dst[y:y+h, x:x+w]
        print('X',x1,'\nY',y1,'\nW',w1,'\nH',h1)
        outfile = img_found + '_undistorted.png'
        print('Undistorted image written to: %s' % outfile)
        cv2.imwrite(outfile, dst)
    #cammtxByteArray = bytearray(cameraMatrix)
    #distByteArray=bytearray(distCoefs)

    #matrixFile.write(cammtxByteArray)
    #matrixFile.write(distByteArray)

    cv2.destroyAllWindows()
