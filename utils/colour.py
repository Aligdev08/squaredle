from pygame import Color


def darken(colour: Color):
    return Color(max(0, colour.r - 50), max(0, colour.g - 50), max(0, colour.b - 50))
