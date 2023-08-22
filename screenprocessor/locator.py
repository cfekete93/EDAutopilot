#!/bin/python3

# Standard libs
from collections import namedtuple
import time
import os

# Keyboard/mouse control, does it support joysticks?
import pyautogui as gui

# Screen capturing and image processing
import matplotlib
import numpy as np
from PIL import ImageGrab # Used for pulling images from the screen?
import cv2 as cv

from .collector.capture import screenshot
from ..images import image
from ..utils import colors, shapes


# TODO [Chris]: Refactor - Irrelevant functionality to current module, move to separate module/package
# Gloabls
last_time = time.time()
os.chdir(os.path.dirname(os.path.abspath(__file__)))
min_tl = shapes.Point(1920, 1080)
max_br = shapes.Point(0, 0)


# TODO [Chris]: Refactor - Irrelevant functionality to current module, move to separate module/package
def preview_screen(bbox=None, windowName='Window name here', cursor_show=True, full_size=False):
    _init(windowName)
    while (True):
        # screen = cv.cvtColor(np.array(ImageGrab.grab(bbox)), cv.COLOR_BGR2RGB)
        screen = screenshot()

        overlay_orientation_box(screen, debug=True)
        overlay_cursor_cross(screen, cursor_show)
        
        show_preview(screen, windowName)
        print_latency()

        if cv.waitKey(25) & 0xFF == ord('q'):
            cv.destroyAllWindows()
            print_latency(True)
            break


# TODO [Chris]: Refactor - Irrelevant functionality to current module, move to separate module/package
def _init(window_name):
    global last_time
#    cv.namedWindow('Screen Name Here', cv.WINDOW_NORMAL)
    cv.namedWindow(window_name)
    cv.moveWindow(window_name, 1920//4, 300)
    last_time = time.time()


# TODO [Chris]: Refactor - Irrelevant functionality to current module, move to separate module/package
def show_preview(screen, window_name, enable=True, full_size=False):
    if not enable:
        return

    if full_size:
        cv.imshow(window_name, screen)
    else:
        preview = cv.resize(screen, (960, 540))
        cv.imshow(window_name, preview)
    #cv.imshow('Orientation Template', image.Template1)


# TODO [Chris]: Refactor - Irrelevant functionality to current module, move to separate module/package
def overlay_cursor_cross(screen, enable=True):
    if not enable:
        return

    cursor = gui.position()
    cursor = gui.Point(cursor.x - 1920, cursor.y)
    cv.drawMarker(screen, cursor, colors.PINK, cv.MARKER_CROSS)


# TODO [Chris]: Refactor - Irrelevant functionality to current module, move to separate module/package
def overlay_orientation_box(screen, search_area=shapes.Box(540, 750, 340, 275), enable=True, debug=True, cutoff: float = .3):
    if not enable:
        return

    global min_tl, max_br

    # Subwindow determined through experimentation, add some padding
    #mtl: shapes.Point(x=612, y=771), mbr: shapes.Point(x=831, y=960)
    #mtl: shapes.Point(x=562, y=735), mbr: shapes.Point(x=863, y=970)

    #search_area = shapes.Box(540, 750, 340, 275)
    #search_area = shapes.Box(0, 0, 0, 0)

    tl, br, confidence = find_object(screen, image.Template1, subsection=search_area)
    if debug:
        if confidence > cutoff:
            if tl.x < min_tl.x:
                min_tl = shapes.Point(tl.x, min_tl.y)
            if tl.y < min_tl.y:
                min_tl = shapes.Point(min_tl.x, tl.y)
            if br.x > max_br.x:
                max_br = shapes.Point(br.x, max_br.y)
            if br.y > max_br.y:
                max_br = shapes.Point(max_br.x, br.y)
        print_info("t1: {}, br: {}, mtl: {}, mbr: {}, confidence: {}   ".format(tl, br, min_tl, max_br, confidence))
    if confidence > cutoff:
        cv.rectangle(screen, tl, br, color=colors.GREEN, thickness=2, lineType=cv.LINE_4)
    if debug:
        search_area_tl = shapes.Point(search_area.x, search_area.y)
        search_area_br = shapes.Point(search_area.x + search_area.w, search_area.y + search_area.h)
        cv.rectangle(screen, search_area_tl, search_area_br, color=colors.YELLOW, thickness=2)
        cv.rectangle(screen, min_tl, max_br, color=colors.RED, thickness=2)


def find_object(
        search_image,
        template_to_locate,
        subsection: shapes.Box = shapes.Box(0, 0, 0, 0),
        match_operation=cv.TM_CCOEFF_NORMED) -> tuple[shapes.Point, shapes.Point, float]:
    """Locate the top-left corner of a template image in a search image or a subsection, if provided.

    Args:
        search_image:
        template_to_locate:
        subsection:
        match_operation:

    Returns:

    """
    if subsection.w <= 0 or subsection.h <= 0:
        subsection = shapes.Box(0, 0, 0, 0)
        search_area = search_image
    else:
        (x, y, w, h) = subsection
        search_area = search_image[y:y + h, x:x + w]

    top_left, confidence = _find_object(search_area, template_to_locate, match_operation)

    (w, h) = get_dimension(template_to_locate)
    top_left = shapes.Point(subsection.x + top_left.x, subsection.y + top_left.y)
    bottom_right = shapes.Point(top_left.x+w, top_left.y+h)

    return top_left, bottom_right, confidence


def _find_object(search_image, template_to_locate, match_operation):
    result = cv.matchTemplate(search_image, template_to_locate, match_operation)
    _, confidence, _, location = cv.minMaxLoc(result)
    location = shapes.Point(*location)
    return location, confidence


def _find_objects():
    pass


def get_cursor_point():
    return gui.position()


def get_cursor_square(half_length=62):
    cursor = get_cursor_point()
    top_left = gui.Point(cursor[0] - half_length, cursor[1] - half_length)
    bottom_right = gui.Point(cursor[0] + half_length, cursor[1] + half_length)
    return top_left, bottom_right


# TODO [Chris]: Refactor - Irrelevant functionality to current module, move to separate module/package
def get_dimension(image):
    return shapes.Dimension(image.shape[1], image.shape[0])


# TODO [Chris]: Refactor - Irrelevant functionality to current module, move to separate module/package
def print_info(message):
    print(message, end='')


# TODO [Chris]: Refactor - Irrelevant functionality to current module, move to separate module/package
def print_latency(end=False):
    if end:
        print()
        return
    
    global last_time
    new_time = time.time()
    print('Loop FPS {}               '.format(1/(new_time-last_time)), end='\r')
    last_time = new_time


# TODO [Chris]: Refactor - Irrelevant functionality to current module, move to separate module/package
def print_line_current_test(message=""):
    print(message, end="\r")
