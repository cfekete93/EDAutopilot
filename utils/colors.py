#!/bin/python3

from collections import namedtuple

Color = namedtuple("Color", "b g r")
ColorStandard = namedtuple("ColorStandard", "r g b")

RED     = Color(0, 0, 255)
GREEN   = Color(0, 255, 0)
BLUE    = Color(255, 0, 0)
WHITE   = Color(255, 255, 255)
BLACK   = Color(0, 0, 0)
PINK    = Color(255, 0, 255)
CYAN    = Color(255, 255, 0)
YELLOW  = Color(0, 255, 255)


def convert_to_rgb(color: Color) -> ColorStandard:
    return ColorStandard(color.r, color.g, color.b)


def convert_to_bgr(color: ColorStandard) -> Color:
    return Color(color.b, color.g, color.r)
