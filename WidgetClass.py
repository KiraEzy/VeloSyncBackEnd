import gpxpy
import numpy as np

import GPXUtil


class WidgetBaseClass:
    def __init__(self, canvas_object , gpx_object, offset):
        self.canvas_object = canvas_object
        self.gpx_object = gpx_object
        self.offset = offset

    # make a abstract method called draw that will be implemented by the child classes
    def draw(self):
        pass
