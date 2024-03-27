import xml.etree.ElementTree as ET

from Util.XMLToDict import XmlDictConfig


class Style:
    def __init__(self, style_path):
        # read xml file
        self.style_path = style_path
        self.style = self.read_style(style_path)

    def render(self):

        return self.video

    def read_style(self, style_path):
        tree = ET.parse(style_path)
        root = tree.getroot()
        xmldict = XmlDictConfig(root)
        return xmldict

    def styleFileToWidgetList(self):
        widgetList = []
        for widget in self.style.get('display').get('item'):
            if widget.get('metric') == 0:
                print('power widget')
                widgetList.append('power')
            elif widget.get('metric') == 1:
                print('heartrate')
                widgetList.append('heartrate')
            elif widget.get('metric') == 2:
                print('cadence')
                widgetList.append('cadence')
            elif widget.get('metric') == 3:
                print('elevation')
                widgetList.append('elevation')
        pass