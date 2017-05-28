"""
Author: Mikael
Script that seraches each quadrant in supplied frame for red markings(supposed to be court corners)
returns xList and yList with coordinates for all four corners found

"""

import numpy as np
import cv2
import imutils

xlist = []
ylist = []

class FindEdge:

    def __init__(self, colorLower, colorUpper):
        self.colorLower = colorLower
        self.colorUpper = colorUpper


        """
        creates a ROI of the specified corner of the supplied frame
        params: number representing a corner in frame, frame
        returns: black frame with ROI in designated corner of original frame
        """
    def get_Masker(self, number, frame):
        if (number == 0):
            black1 = cv2.rectangle(self.black,(0,(frame.shape[0]/2)),((frame.shape[1]/2),frame.shape[0]),(255, 255, 255), -1)
            return black1
        elif(number == 1):
            black1 = cv2.rectangle(self.black,((frame.shape[1]/2),(frame.shape[0]/2)),((frame.shape[1]),frame.shape[0]),(255, 255, 255), -1)
            return black1
        elif(number == 2):
            black1 = cv2.rectangle(self.black,((frame.shape[1]/2),0),((frame.shape[1]),frame.shape[0]/2),(255, 255, 255), -1)
            return black1
        elif(number == 3):
            black1 = cv2.rectangle(self.black,(0,0),((frame.shape[1]/2),frame.shape[0]/2),(255, 255, 255), -1)
            return black1

    """
    Finds the center of the cornermark, one in each quadrant of the frame, returns one list of x-values and one list of y-values
    params: frame
    return xList, yList coordinates for each corner
    """
    def get_edges(self, frame):
        self.frame = frame

        nbr = 0
        #one iteration for each corner of the picture
        while nbr<4:
            frame1=self.frame.copy()
            self.black = np.zeros((frame1.shape[0], frame1.shape[1], 3), np.uint8)
            black1 = self.get_Masker(nbr, self.black)   #creates one ROI containing one corner of the frame per iteration
            gray = cv2.cvtColor(black1,cv2.COLOR_BGR2GRAY)  #---converting to gray

            ret,b_mask = cv2.threshold(gray,127,255, 0)

            hsv = cv2.cvtColor(frame1, cv2.COLOR_RGB2HSV)
            mask = cv2.inRange(hsv, self.colorLower, self.colorUpper)
            mask = cv2.erode(mask, None, iterations=1)
            mask = cv2.dilate(mask, None, iterations=2)
            mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, None)
            mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, None)
            #AND-operation with the ROI to filter out the rest of the frame
            fin = cv2.bitwise_and(mask,mask,mask = b_mask)
            cv2.imshow("fin", fin)
            #fetch found countures into cnts
            cnts = cv2.findContours(fin.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
            cX = 0
            cY = 0
            for c in cnts:
                M = cv2.moments(c)
                cX += float(M["m10"] / M["m00"])
                cY += float(M["m01"] / M["m00"])
                cv2.drawContours(frame1, [c], -1, (0, 255, 0), 2)
                cv2.circle(frame1, (int(cX), int(cY)), 2, (255, 255, 255), -1)
                cv2.putText(frame1, "center", (int(cX) - 20, int(cY) - 20),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
                cv2.imshow("frame", frame1)
            k = cv2.waitKey(0)
            if k == 32: #om mellanslag trycks ned
                #put the average of each centerpoint found within the countour in the list
                xlist.append(float(cX/len(cnts)))
                ylist.append(float(cY/len(cnts)))
                pass
            elif k == 27:#esc to break
                break
            nbr += 1

        cv2.destroyAllWindows()
        return xlist, ylist
