#!/bin/python3

# Standard libs
import time
import os

# Keyboard/mouse control, does it support joysticks?
import pyautogui as gui

# Screen capturing and image processing
import numpy as np
from PIL import ImageGrab  # Used for pulling images from the screen?
import cv2 as cv

from images import image
from utils import colors
from utils.console.printers import slp
from screenprocessor.collector.capture import screenshot, screenshot_test

# import locator

# Gloabls
last_time = time.time()
os.chdir(os.path.dirname(os.path.abspath(__file__)))

    
def find_single_object():
    # Uses matchTemplate function in OpenCV library under the hood
    # ExampleResult1 = gui.locateOnScreen('images/orientation.png', confidence=0.9)
    result = cv.matchTemplate(image.Example1, image.Template1, cv.TM_CCOEFF_NORMED)

    # Get dimensions of Template
    template_width = image.Template1.shape[1]
    template_height = image.Template1.shape[0]

    # Get location with the lowest/highest probabilties
    min_val, max_val, min_location, max_location = cv.minMaxLoc(result)

    # Get box around result
    top_left = max_location
    bottom_right = (top_left[0] + template_width, top_left[1] + template_height)

    # Overlay green box over found image
    cv.rectangle(image.Example1, top_left, bottom_right, color=colors.GREEN, thickness=2, lineType=cv.LINE_4)

    # Display results and exit upon registering keypress
    cv.imshow('Navigation Icon - Search Results', image.Example1)
    cv.imwrite('result.png', image.Example1)
    cv.waitKey()


def find_multiple_objects(threshold=0.9):
    result = cv.matchTemplate(image.Example1, image.Template1, cv.TM_CCOEFF_NORMED)

    # Get dimensions of Template
    template_width = image.Template1.shape[1]
    template_height = image.Template1.shape[0]

    # Get all x,y coordinates where element >= threshold
    locations = np.where(result >= threshold)
    # Inside-Out, reverse list, (*) unpack outer list, (zip) make generator that combines each n-th element into
    # tuple, make list of tuples
    locations = list(zip(*locations[::-1]))

    rectangles = []
    for location in locations:
        rectangle = [int(location[0]), int(location[1]), template_width, template_height]
        rectangles.append(rectangle)
        rectangles.append(rectangle) # Prevents groupRectangles from removing results with only one box

    # 1 - min # of rectangles to group, eps -> smaller (closer) the rectangles need to be to group and vice versa
    rectangles, weights = cv.groupRectangles(rectangles, 1, eps=0.5)
    
    if len(rectangles) > 0:
        for (x, y, w, h) in rectangles:
            top_left = (x, y)
            bottom_right = (x+w, y+h)

            # Draw boxes
            cv.rectangle(image.Example1, top_left, bottom_right, colors.GREEN, lineType=cv.LINE_4)

            # Draw cross in middle of boxes
            center = (x + int(w/2), y + int(h/2))
            cv.drawMarker(image.Example1, center, colors.PINK, cv.MARKER_CROSS)
        
        cv.imshow('Matches', image.Example1)
        cv.waitKey()


def screen_capture_test(bbox=None, cursor_box=True, shrink=True):
    global last_time
#    cv.namedWindow('Screen Name Here', cv.WINDOW_NORMAL)
    last_time = time.time()
    while True:
        slp.print('', clear=True)
        # screen = screenshot(bbox)
        screen = screenshot_test()
        slp.print('screen type: {st} '.format(st=type(screen).__name__))
        # screen = np.array(ImageGrab.grab(bbox))
        if cursor_box:
            cursor = gui.position()
            cursor = gui.Point(cursor.x - 1920, cursor.y)  # Parameterize but for now this is because using middle
            tl, br = get_cursor_rect(cursor)
            cv.rectangle(screen, tl, br, colors.RED, thickness=2)
        if shrink:
            preview = cv.resize(screen, (960, 540))
            cv.imshow('Screen Name Here', preview)
        else:
            cv.imshow('Screen Name Here', screen)
        print_latency()
        if cv.waitKey(25) & 0xFF == ord('q'):
            cv.destroyAllWindows()
            slp.print('', newline=True)
            break


def alternative_screencapture_test():
    while True:
        screenshot = gui.screenshot()  # Only captures left screen
        screenshot = np.array(screenshot)  # OpenCV needs a numpy array
        screenshot = cv.cvtColor(screenshot, cv.COLOR_RGB2BGR) # Needed because OpenCV is BGR by default
        (h, w) = screenshot.shape[:2]

        preview = cv.resize(screenshot, (w//2, h//2))
        cv.imshow('Pyautogui Screencapture Test', preview)
        # cv.imshow('Pyautogui Screencapture Test', screenshot)

        if cv.waitKey(1) == ord('q'):
            cv.destroyAllWindows()
            break


# Eventually capture screenshots of specific windows (ie. windows that belong to the game), OS specific
def x11_window_capture():
    from Xlib import display as sys_display
    display = sys_display.Display()
    root = display.screen().root


def mousetrack_capture(box_size=125, window_name="Preview"):
    global last_time
    last_time = time.time()
    started=False
    while True:
        cursor = gui.position()
        tl, br = get_cursor_rect(cursor, offset=box_size)
        box = (tl.x, tl.y, br.x, br.y)
        screen = cv.cvtColor(np.array(ImageGrab.grab(box)), cv.COLOR_BGR2RGB)
        # screen = np.array(ImageGrab.grab(bbox))
        if not started:
            cv.namedWindow(window_name)
            cv.moveWindow(window_name, (5*1920)//2, 300)
            started = True
        cv.imshow(window_name, screen)
        print_latency()
        key_press = cv.waitKey(25)
        if key_press & 0xFF == ord('q'):
            reply = gui.confirm(text="Do you wish to quit?", title="Quit?", buttons=["Yes", "No"])
            if reply == "Yes":
                cv.destroyAllWindows()
                print_latency(True)
                break
        if key_press & 0xFF == ord('p'):
            gui.alert(text="You are paused! Press 'OK' to resume.", title="Paused!", button="OK")


def get_cursor_rect(cursor, offset=62):
    top_left = gui.Point(cursor[0]-offset, cursor[1]-offset)
    bottom_right = gui.Point(cursor[0]+offset, cursor[1]+offset)
    return top_left, bottom_right


def print_latency():
    global last_time
    new_time = time.time()
    slp.print('Loop latency {} seconds'.format(1/(new_time-last_time)))
    last_time = new_time
