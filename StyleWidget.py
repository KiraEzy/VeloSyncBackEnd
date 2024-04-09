import xml.etree.ElementTree as ET

from Util.XMLToDict import XmlDictConfig
from Widgets.ElevationWidget import ElevationWidget


class Style:
    def __init__(self, style_path, canvas_object):
        # read xml file
        self.style_path = style_path
        self.styleXML = self.read_style(style_path)

        self.canvas = canvas_object

    def read_style(self, style_path):
        tree = ET.parse(style_path)
        root = tree.getroot()
        xmldict = XmlDictConfig(root)
        return xmldict

    def styleFileToWidgetList(self):
        widgetList = []
        isOne = False
        for widget in self.styleXML.get('display').get('item'):
            if type(widget) == str:
                isOne = True
            if isOne:
                widget = self.styleXML.get('display').get('item')
            if int(widget['metric']) == 0:
                print('power widget')
                widgetList.append('power')
            elif int(widget['metric']) == 1:
                print('heartrate')
                widgetList.append('heartrate')
            elif int(widget['metric']) == 2:
                print('cadence')
                widgetList.append('cadence')
            elif int(widget['metric']) == 3:
                print('elevation')
                wid = ElevationWidget(self.canvas, self.canvas.gpx_object, (widget['posx'], widget['posy']), widget['theme'], widget['color'], (widget['width'], widget['height']))
                widgetList.append('elevation')
            if isOne:
                break
        return widgetList