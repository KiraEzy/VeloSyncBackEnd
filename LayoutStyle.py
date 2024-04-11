import xml.etree.ElementTree as ET

from Util.XMLToDict import XmlDictConfig
from Widgets.ElevationWidget import ElevationWidget


class LayoutStyle:
    def __init__(self, layout_path, canvas_object):
        # read xml file
        self.layout_path = layout_path
        self.layoutXML = self.read_layout(layout_path)

        self.canvas = canvas_object

    def read_layout(self, layout_path):
        tree = ET.parse(layout_path)
        root = tree.getroot()
        xmldict = XmlDictConfig(root)
        return xmldict
    def read_style(self, style_path):
        tree = ET.parse(style_path)
        root = tree.getroot()
        xmldict = XmlDictConfig(root)
        return xmldict

    def layoutFileToWidgetList(self):
        widgetList = []
        isOne = False
        for widget in self.layoutXML.get('display').get('item'):
            if type(widget) == str:
                isOne = True
            if isOne:
                widget = self.layoutXML.get('display').get('item')
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