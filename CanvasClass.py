from datetime import time

import time

import numpy as np
from PIL import Image, ImageFont, ImageDraw
import cv2
import GPXUtil
import LayoutStyle
from GPXClass import GPXClass


class Canvas:
    def __init__(self, video_path, layout_path, gpx_path, output_path, start_frame):
        self.gpx_object = GPXClass(gpx_path)
        self.style = LayoutStyle.LayoutStyle(layout_path, self)
        self.video = video_path
        self.widget_list = self.style.layoutFileToWidgetList()
        self.output_path = output_path
        self.start_frame = start_frame

    def render(self):
        cap = cv2.VideoCapture(self.video)
        fps = cap.get(cv2.CAP_PROP_FPS)
        interval_in_fps = self.gpx_object.datapoint_interval * fps
        last_frame = interval_in_fps
        self.currDatapointIndex = 0
        curr_datapoint = self.gpx_object.datapoints[self.currDatapointIndex]
        frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(self.output_path, fourcc, fps, (frame_width, frame_height))

        frame_counter = 0
        self.start_time = time.time()

        self.width = cap.get(3)  # float `width`
        self.height = cap.get(4)  # float `height`

        frame_time_array = []
        while cap.isOpened():
            # Read the current frame
            ret, frame = cap.read()

            if ret:
                # Process the frame (add number)
                frame_counter += 1
                if frame_counter >= last_frame:
                    self.currDatapointIndex += 1
                    last_frame = frame_counter + interval_in_fps
                if frame_counter >= self.start_frame:
                    pil_image = Image.fromarray(frame)
                    self.draw = ImageDraw.Draw(pil_image, "RGBA")
                    frame_StartTime = time.time()                               #logging use

                    if frame_counter == self.start_frame:
                        current_time = cap.get(cv2.CAP_PROP_POS_MSEC) / 1000.0  #logging use
                        print("Current Time:", current_time)
                        cv2.imwrite('./Output/starting_frame.jpg', frame)
                    # Write the modified frame to the output video

                    # Draw non-ascii text onto image
                    font = ImageFont.truetype("C:\\Github\\VeloSyncBackEnd\\font\\Oswald-VariableFont_wght.ttf", 35)
                    strokeWidth = 2,
                    fill_color = (0, 0, 0)
                    stroke_color = (255, 255, 255)

                    for widget in self.widget_list:
                        widget.drawFrame()
                    # draw.text((50, 80), "Power: " + str(curr_datapoint.extensions[0].text) + "Watts", font=font,
                    #           fill=fill_color, stroke_width=1, stroke_fill=stroke_color)
                    # draw.text((50, 150), "Elevation: " + str(curr_datapoint.elevation) + "km", font=font,
                    #           fill=fill_color, stroke_width=1, stroke_fill=stroke_color)
                    # draw.text((50, 250), "Velocity: " + str(curr_datapoint.velocity) + "m/s", font=font,
                    #           fill=fill_color, stroke_width=1, stroke_fill=stroke_color)
                    # draw.text((50, 350),
                    #           "Lat: " + str(curr_datapoint.latitude) + "Long: " + str(curr_datapoint.longitude),
                    #           font=font, fill=fill_color, stroke_width=1, stroke_fill=stroke_color)
                    # draw.line(path_line_coord, fill=(255, 255, 255), width=2)
                    # draw.ellipse(
                    #     xy=[(path_line_coord[self.currDatapointIndex][0] - 5, path_line_coord[self.currDatapointIndex][1] - 5),
                    #         (path_line_coord[self.currDatapointIndex][0] + 5, path_line_coord[self.currDatapointIndex][1] + 5)],
                    #     fill=(255, 0, 0), outline=(255, 255, 255), width=2)
                    # drawElevationGraph(draw, elevationGraphData[0], elevationGraphData[1], elevationGraphData[2],
                    #                    elevationGraphData[3], elevationGraphData[4], elevationGraphData[5],
                    #                    self.currDatapointIndex)
                    # Convert back to Numpy array and switch back from RGB to BGR
                    frame = np.asarray(pil_image)

                    out.write(frame)
                    print('Frame:', frame_counter)
                    current_time = cap.get(cv2.CAP_PROP_POS_MSEC) / 1000.0
                    print("Current Time:", current_time)
                    # Display the frame (optional)
                    cv2.imshow('Frame', frame)
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break
                    frame_EndTime = time.time()
                    frame_time_array.append(frame_EndTime - frame_StartTime)
                    print('Frame Time:', frame_EndTime - frame_StartTime)
                    print('Frame Avg Time:', np.sum(frame_time_array), "/", len(frame_time_array), " = ",
                          np.sum(frame_time_array) / len(frame_time_array))
            else:
                break

        cap.release()
        out.release()
        cv2.destroyAllWindows()

        end_time = time.time()
        elapsed_time = end_time - self.start_time
        print('Time used:', elapsed_time, 'seconds')
        return self.video
