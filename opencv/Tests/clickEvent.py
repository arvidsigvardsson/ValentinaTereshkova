import cv2

refPt = []

"""
Enables the registering mouseclicks, function doesnt need to be called upon
"""
def click_event(event, x, y, flags, param):
    global refPt
    if event == cv2.EVENT_LBUTTONDOWN:
        refPt.append((x,y))
        print(refPt)

class pointFinder:
    """
    Creates a new pointFinder object, no params needed
    """
    def __init__(self):
        self = self
    """
    finds the (x,y)-coordinates in an image when pressing left mousebutton, when 2 points are clicked in the image the function returns the (x,y) - coordinates for the points.
    Param: Image - Path to the image
    """
    def findPoints(self, image):
        image = cv2.imread(image, 1)
        cv2.namedWindow('window')
        cv2.setMouseCallback('window', click_event)

        cv2.imshow('window',image)
        key = cv2.waitKey(1) & 0xFF

        if len(refPt) == 2 or cv2.waitKey(0):
            cv2.destroyAllWindows()
            return refPt[0], refPt[1]
