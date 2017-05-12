import sys
import numpy as np
import cv2

import calibration

def main():
    # print sys.argv[1]

    infile = sys.argv[1]
    outfile = infile + '_nodistortion.jpg'

    in_image = cv2.imread(infile)

    h, w = in_image.shape[:2]
    newcameramatrix, roi = cv2.getOptimalNewCameraMatrix(

    

if __name__ == '__main__':
    main()
