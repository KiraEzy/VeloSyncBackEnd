import gpxpy
import numpy as np

import GPXUtil


class CanvasBaseClass:
    def __init__(self, video, style, gpx_object, widget_list = []):
        self.widget_list = widget_list
        self.gpx_object = gpx_object
        self.style = style
        self.video = video

    def render(self):

        return self.video
