from IpCamera import IpCam, cv2, np

url = 'http://192.168.20.149/axis-cgi/mjpg/video.cgi'

ipcam = IpCam(url)
ipcam.start()

while True:
    frame = ipcam.getFrame()

    if frame == None:
        continue
    else:
        cv2.imshow('frame', frame)
        k = cv2.waitKey(1) & 0xFF
        if k==27:
            break


    # frame = np.fromstring(str1, dtype=np.uint8)
    # if frame == None:
    #     print('Camera None')
    # else:
    #     print('Camera found')
    # cv2.imshow('frame1', frame)
    # k = cv2.waitKey(5) & 0xFF
    # if k==27:
    #     break

    # bytes = ipcam.getFrame
    # jpg = bytes[a:b+2]
    # bytes = bytes[b+2:]
    # frame = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8),cv2.IMREAD_COLOR)
    # cv2.imshow('cam', frame)
    # if cv2.waitKey(1) == 27:
    #     exit(0)
    #     cv2.destroyAllWindows()






# def click_event(event, x, y, flags, param):
#     global refPt
#     if event == cv2.EVENT_LBUTTONDOWN:
#         print('hello')
#         refPt.append((x,y))
#
#     #elif event == cv2.EVENT_LBUTTONUP:
#     #    print('hello1')
#     #    refPt.append((x, y))
#
#     print(refPt)
#
#
# image = cv2.imread('test.jpg', 1)
# cv2.namedWindow('window')
#
# cv2.setMouseCallback('window', click_event)
#
# clicks = 0
#
# refPt = []
#
#
# #while clicks < 3:
# cv2.imshow('window',image)
# key = cv2.waitKey(1) & 0xFF
#
#     #print(refPt[0])
#     #print(refPt[1])
#
# # if key == ord("c"):
# #      break
#
#
# if cv2.waitKey(0):
#     cv2.destroyAllWindows()
