#!/bin/python3

import os

import cv2 as cv

# Original images will be used without any preprocessing
Example1 = cv.imread(os.path.dirname(os.path.abspath(__file__))+'/test2.png', cv.IMREAD_UNCHANGED)
Template1 = cv.imread(os.path.dirname(os.path.abspath(__file__))+'/orientation.png', cv.IMREAD_UNCHANGED)

# Use images but shrink height/width in half
Example1Halved = cv.imread(os.path.dirname(os.path.abspath(__file__))+'/test2.png', cv.IMREAD_REDUCED_COLOR_2)
Template1Halved = cv.imread(os.path.dirname(os.path.abspath(__file__))+'/orientation.png', cv.IMREAD_REDUCED_COLOR_2)
