#!/usr/bin/env python

'''
camera calibration for distorted images with chess board samples
reads distorted images, calculates the calibration and write undistorted images

usage:
    calibrate.py [--debug <output path>] [--square_size] [<image mask>]

default values:
    --debug:    ./output/
    --square_size: 1.0
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
    pic_url='http://192.168.20.149/jpg/image.jpg?size=3'
    #while counter <10:
    matrixFile = open("MatrixAndCoefs.txt", "wb")

    while counter < 10:
        img_data = requests.get(pic_url).content
        frame = cv2.imdecode(np.fromstring(img_data, dtype=np.uint8),cv2.IMREAD_COLOR)
        cv2.imshow('frame', frame)
        k = cv2.waitKey(10) & 0xFF
        if k == 32:
            name = './test/pic'+str(counter)+'.jpg'
            #img_data = requests.get(pic_url).content
            with open(name, 'wb') as handler:
                handler.write(img_data)
                counter += 1
                time.sleep(1)
                print('bild: '+str(counter))


    args, img_mask = getopt.getopt(sys.argv[1:], '', ['debug=', 'square_size='])
    args = dict(args)
    args.setdefault('--debug', './output/')
    args.setdefault('--square_size', 1.0)


    if not img_mask:
        img_mask = './test/pic*.jpg'  # default
    else:
        img_mask = img_mask[0]

    img_names = glob(img_mask)
    debug_dir = args.get('--debug')
    if not os.path.isdir(debug_dir):
        os.mkdir(debug_dir)
    square_size = float(args.get('--square_size'))

    pattern_size = (7, 7)
    pattern_points = np.zeros((np.prod(pattern_size), 3), np.float32)
    pattern_points[:, :2] = np.indices(pattern_size).T.reshape(-1, 2)
    pattern_points *= square_size

    obj_points = []
    img_points = []
    h, w = 0, 0
    img_names_undistort = []
    for fn in img_names:
        print('processing %s... ' % fn, end='')
        img = cv2.imread(fn, 0)
        if img is None:
            print("Failed to load", fn)
            continue

        h, w = img.shape[:2]
        found, corners = cv2.findChessboardCorners(img, pattern_size)
        if found:
            term = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_COUNT, 30, 0.1)
            cv2.cornerSubPix(img, corners, (5, 5), (-1, -1), term)

        if debug_dir:
            vis = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
            cv2.drawChessboardCorners(vis, pattern_size, corners, found)
            path, name, ext = splitfn(fn)
            outfile = debug_dir + name + '_chess.png'
            cv2.imwrite(outfile, vis)
            if found:
                img_names_undistort.append(outfile)

        if not found:
            print('chessboard not found')
            continue

        img_points.append(corners.reshape(-1, 2))
        obj_points.append(pattern_points)

        print('ok')


    # calculate camera distortion
    rms, camera_matrix, dist_coefs, rvecs, tvecs = cv2.calibrateCamera(obj_points, img_points, (w, h), None, None)

    print("\nRMS:", rms)
    print("camera matrix:\n", camera_matrix)
    print("distortion coefficients: ", dist_coefs)

    # undistort the image with the calibration
    print('')
    for img_found in img_names_undistort:
        img = cv2.imread(img_found)

        h,  w = img.shape[:2]
        print("H W",h,w)
        newcameramtx, roi = cv2.getOptimalNewCameraMatrix(camera_matrix, dist_coefs, (w, h), 1, (w, h))
        print("NEW camera matrix:\n", newcameramtx)
        dst = cv2.undistort(img, camera_matrix, dist_coefs, None, newcameramtx)

        # crop and save the image
        x, y, w, h = roi
        x1,y1,w1,h1 = (x, y, w, h)

        dst = dst[y:y+h, x:x+w]
        print('X',x1,'\nY',y1,'\nW',w1,'\nH',h1)
        outfile = img_found + '_undistorted.png'
        print('Undistorted image written to: %s' % outfile)
        cv2.imwrite(outfile, dst)
    #cammtxByteArray = bytearray(camera_matrix)
    #distByteArray=bytearray(dist_coefs)

    #matrixFile.write(cammtxByteArray)
    #matrixFile.write(distByteArray)

    cv2.destroyAllWindows()
