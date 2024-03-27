import gpxpy
import numpy as np

import GPXUtil
import StyleWidget
from GPXClass import GPXClass


class Canvas:
    def __init__(self, video_path, style_path, gpx_path):
        self.gpx_object = GPXClass(gpx_path)
        self.style = StyleWidget.Style(style_path)
        self.video = video_path
        self.widget_list = styleFileToWidgetList(self.style)
    def render(self):

        return self.video
