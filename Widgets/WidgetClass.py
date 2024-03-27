import gpxpy
import numpy as np

import GPXUtil


from abc import ABC, abstractmethod

class WidgetBase(ABC):
    def __init__(self, canvas_object, gpx_object, offset, theme, color):
        self.canvas_object = canvas_object
        self.gpx_object = gpx_object
        self.offset = offset
        self.theme = theme
        self.color = color

    @abstractmethod
    def draw(self):
        pass