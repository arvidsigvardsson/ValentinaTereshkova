import cv2

refPt = []

def click_event(event, x, y, flags, param):
    global refPt
    #refPt = []
    if event == cv2.EVENT_LBUTTONDOWN:
        #print('hello')
        refPt.append((x,y))
        print(refPt)

class pointFinder:

    def __init__(self):
        self = self

    def findPoints(self, image):
        image = cv2.imread(image, 1)
        cv2.namedWindow('window')
        cv2.setMouseCallback('window', click_event)

        cv2.imshow('window',image)
        key = cv2.waitKey(1) & 0xFF

        if len(refPt) == 2 or cv2.waitKey(0):
            cv2.destroyAllWindows()
            return refPt[0], refPt[1]
