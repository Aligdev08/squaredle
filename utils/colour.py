from pygame import Color


def darken(colour: Color):
    return Color(max(0, colour.r - 20), max(0, colour.g - 20), max(0, colour.b - 20))
