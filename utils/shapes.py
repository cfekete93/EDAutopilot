#!/bin/python3

from collections import namedtuple

Point = namedtuple("Point", "x y")
"""2D spacial coordinate"""

Dimension = namedtuple("Dimension", "w h")
"""Represent a generic region with size w x h"""

Box = namedtuple("Box", "x y w h")
"""Represent a region fixed with x,y in top-left corner with dimensions w X h"""

BoxPoints = namedtuple("BoxPoints", "x1 y1 x2 y2")
"""Represent a region with corners at x1,y1 and x2,y2"""


def get_box(point: Point, size: Point | Dimension) -> Box:
    x, y = point
    if isinstance(size, Point):
        x2, y2 = size
        w = x2 - x
        h = y2 - y
    elif isinstance(size, Dimension):
        w, h = size
    else:
        raise TypeError('size must be Point or Dimension')
    return Box(x, y, w, h)


def get_box_points(point: Point, size: Point | Dimension) -> BoxPoints:
    x1, y1 = point
    if isinstance(size, Point):
        x2, y2 = size
    elif isinstance(size, Dimension):
        w, h = size
        x2 = x1 + w
        y2 = y1 + h
    else:
        raise TypeError('size must be Point or Dimension')
    return BoxPoints(x1, y1, x2, y2)
