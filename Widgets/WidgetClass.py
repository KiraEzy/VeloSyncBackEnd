import gpxpy
import numpy as np

import GPXUtil


from abc import ABC, abstractmethod

class WidgetBase(ABC):
    def __init__(self, canvas_object, gpx_object, offset, theme, color, size):
        self.canvas_object = canvas_object
        self.gpx_object = gpx_object
        self.offset = offset
        self.theme = theme
        self.themeXML = self.getStyleById(theme)
        self.color = color
        self.size = size # Size of the widget in % of the canvas size such as (0.4, 0.15) for 40% width and 15% height

    def getStyleById(self, id):
        xml = self.read_style("./StylesInfo.xml")
        return self.layoutXML.get('style').get(id)
    @abstractmethod
    def drawFrame(self):
        pass

    @abstractmethod
    def getGraph(self):
        pass