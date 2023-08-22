#!/bin/python3

# System libraries
from time import time

# 3rd party (pip) libraries
import cv2 as cv
import numpy as np
import mss
from PIL import ImageGrab


def screenshot(bbox: tuple[int, int] = None, colorspace: int = cv.COLOR_BGR2RGB) -> np.ndarray:
    with mss.mss() as sct:
        monitor = sct.monitors[1]
        img = sct.grab(monitor)
        return cv.cvtColor(np.array(img), colorspace)
        # return np.array(img)

def screenshot_alt(bbox: tuple[int, int] = None, colorspace: int = cv.COLOR_BGR2RGB) -> np.ndarray:
    return cv.cvtColor(np.array(ImageGrab.grab(bbox)), colorspace)


def screenshot_test():
    return _screenshot_test1()


def _screenshot_test1():
    with mss.mss() as sct:
        monitor = sct.monitors[1]
        img = sct.grab(monitor)
        return cv.cvtColor(np.array(img), cv.COLOR_BGR2RGB)


# Pass in image and use cv.selectROI() function to highlight out section to copy
def selectROI():
    pass
