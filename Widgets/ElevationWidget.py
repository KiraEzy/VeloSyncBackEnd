import numpy as np
from PIL import Image, ImageFont, ImageDraw

from Widgets.WidgetClass import WidgetBase

class ElevationWidget(WidgetBase):
    graph = None
    def drawFrame(self):
        # Implement the draw method according to your specific requirements
        # This method should contain the logic to draw the widget
        if self.graph is None:
            graph = self.getGraph()
            elevationTextMax = graph[0]
            elevationTextMin = graph[1]
            elevationFont = graph[2]
            path_line_coord = graph[3]
            elevationRect = graph[4]
            textMarginLeft = graph[5]
        currDatapointIndex = self.canvas_object.datapointIndex
        # Example implementation:
        print("drawing widget Elevation...")
        text_dim_max = self.draw.textbbox((0, 0), elevationTextMax, font=elevationFont)
        text_dim_min = self.draw.textbbox((0, 0), elevationTextMin, font=elevationFont)
        self.draw.polygon(path_line_coord, fill=(60, 231, 77, 162), width=2)
        self.draw.text((elevationRect[0][0] - (text_dim_max[2] - text_dim_max[0]) - textMarginLeft, elevationRect[0][1] +
                   (text_dim_max[1] - text_dim_max[3])), elevationTextMax, font=elevationFont, stroke_width=1)
        self.draw.text((elevationRect[0][0] - (text_dim_min[2] - text_dim_min[0]) - textMarginLeft, elevationRect[1][1] +
                   (text_dim_min[1] - text_dim_min[3])), elevationTextMin, font=elevationFont, stroke_width=1)
        shape = [(path_line_coord[currDatapointIndex + 1][0], path_line_coord[currDatapointIndex + 1][1]),
                 (path_line_coord[currDatapointIndex][0], elevationRect[1][1])]
        self.draw.line(shape, fill="white", width=5)
        self.draw.rectangle(elevationRect, fill=(255, 255, 255, 127))
        self.draw.ellipse(
            xy=[(path_line_coord[currDatapointIndex + 1][0] - 5, path_line_coord[currDatapointIndex + 1][1] - 5),
                (path_line_coord[currDatapointIndex + 1][0] + 5, path_line_coord[currDatapointIndex + 1][1] + 5)],
            fill=(255, 0, 0), outline=(255, 255, 255), width=2)

    def getGraph(self):
        w= self.canvas_object.width
        h= self.canvas_object.height
        graphSize = self.size
        elevation = self.canvas_object.gpx_object.elevation


        graphCenter = (0.5+self.offset[0], 0.5+self.offset[1])
        graphSize = (w * graphSize[0], h * graphSize[1])
        graphCenter = (w * graphCenter[0], h * graphCenter[1])
        elevationRect = [(graphCenter[0] - graphSize[0] / 2, graphCenter[1] - graphSize[1] / 2),
                         (graphCenter[0] + graphSize[0] / 2, graphCenter[1] + graphSize[1] / 2)]
        elevation_on_scale = (elevation - np.min(elevation)) / (np.max(elevation) - np.min(elevation))
        elevation_on_scale = [(1 - ele) for ele in elevation_on_scale]


        draw_time_coordination = np.linspace(elevationRect[0][0], elevationRect[1][0], len(elevation_on_scale))
        draw_elevation_coordination = [(ele * (elevationRect[1][1] - elevationRect[0][1]) + elevationRect[0][1]) for ele in
                                       elevation_on_scale]

        path_line_coord = list(zip(draw_time_coordination, draw_elevation_coordination))
        path_line_coord.insert(0, (elevationRect[0][0], elevationRect[1][1]))
        path_line_coord.append(elevationRect[1])
        # Draw non-ascii text onto image

        elevationFont = ImageFont.truetype("C:\\Github\\VeloSyncBackEnd\\font\\Oswald-VariableFont_wght.ttf", 25)
        elevationTextMax = str(round(np.max(elevation), 1)) + "m"
        elevationTextMin = str(round(np.min(elevation), 1)) + "m"
        textMarginLeft = 10
        return (elevationTextMax, elevationTextMin, elevationFont, path_line_coord, elevationRect, textMarginLeft)