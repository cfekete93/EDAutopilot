#!/bin/python3

# from quickstart import *
from .screenprocessor import locator


def main():
    locator.preview_screen((1920, 0, 2*1920, 1080))
    # print(gui.size())
    # gui.displayMousePosition()
    # screen_capture_test((1920, 0, 2*1920, 1080))
    # mousetrack_capture()
    # find_single_object()
    # find_multiple_objects()
    # alternative_screencapture_test()


if __name__ == '__main__':
    main()
