import math

import cairocffi as cairo
import numpy


def test_numpy():
    data = numpy.zeros((200, 200, 4), dtype=numpy.uint8)
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, 200, 200, data=data)
    cr = cairo.Context(surface)
    cr.set_source_rgb(1.0, 1.0, 1.0)
    cr.paint()
    cr.arc(100, 100, 80, 0, 2*math.pi)
    cr.set_line_width(3)
    cr.set_source_rgb(1.0, 0.0, 0.0)
    cr.stroke()
