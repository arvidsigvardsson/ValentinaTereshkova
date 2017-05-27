"""
Author: Anton Hellbe, Mikael Nilsson

"""
import numpy as np
import cv2
import requests
import threading
from threading import Thread, Event, ThreadError
import time

class IpCam:

    """
    Initialize ipcamera object
    Params: url to cameras mjpeg stream
    Returns: None
    """
    def __init__(self, url):
        self.stream = requests.get(url, stream=True)
        self.thread_cancelled = False
        self.thread = Thread(target=self.run)
        self.img = None
        print('Init camera done')

    """
    Starts the camerafeed from the IP-camera in a new thread
    """
    def start(self):
        self.thread.start()
        print('Starting camera')

    """
    Self called when using start function.
    Fetches the bytestream from the camera and puts it in a cv2 frame
    """
    def run(self):
        bytes = ''
        while not self.thread_cancelled:
            try:
                bytes += self.stream.raw.read(1024)
                a = bytes.find('\xff\xd8')
                b = bytes.find('\xff\xd9')
                if a != -1 and b != -1:
                    jpg = bytes[a:b+2]
                    bytes = bytes[b+2:]
                    self.img = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8),cv2.IMREAD_COLOR)
            except ThreadError:
                self.thread_cancelled
                self.img = None

    """
    Used for checking if the thread is still running
    """
    def is_running(self):
        return self.thread.isAlive()
    """
    Returns the cv2 frame
    """
    def getFrame(self):
        return self.img
    """
    Shuts down the thread, IMPORTANT: Call this method when closing the program
    """
    def shut_down(self):
        self.thread_cancelled = True
        #block while waiting for thread to terminate
        while self.thread.isAlive():
            time.sleep(1)
        return True
