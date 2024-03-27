# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import time

import numpy as np
from PIL import Image, ImageFont, ImageDraw
import cv2

import CanvasClass
import GPXClass
import GPXUtil


output_path = './Output/output_video.mp4'





def getElevationGraph(w, h, draw, elevation ,graphSize, graphCenter):
    graphSize = (w * graphSize[0], h * graphSize[1])
    graphCenter = (w * graphCenter[0], h * graphCenter[1])
    elevationRect = [(graphCenter[0] - graphSize[0] / 2, graphCenter[1] - graphSize[1] / 2),
                     (graphCenter[0] + graphSize[0] / 2, graphCenter[1] + graphSize[1] / 2)]

    elevation_on_scale = (elevation - np.min(elevation)) / (np.max(elevation) - np.min(elevation))
    elevation_on_scale = [(1 - ele) for ele in elevation_on_scale]

    time_on_scale = np.linspace(0, 1, len(elevation_on_scale))

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

def drawElevationGraph(draw, elevationTextMax, elevationTextMin, elevationFont, path_line_coord, elevationRect, textMarginLeft, currDatapointIndex):
    text_dim_max = draw.textbbox((0, 0), elevationTextMax, font=elevationFont)
    text_dim_min = draw.textbbox((0, 0), elevationTextMin, font=elevationFont)
    draw.polygon(path_line_coord, fill=(60, 231, 77, 162), width=2)
    draw.text((elevationRect[0][0] - (text_dim_max[2] - text_dim_max[0]) - textMarginLeft, elevationRect[0][1] +
               (text_dim_max[1] - text_dim_max[3])), elevationTextMax, font=elevationFont, stroke_width=1)
    draw.text((elevationRect[0][0] - (text_dim_min[2] - text_dim_min[0]) - textMarginLeft, elevationRect[1][1] +
               (text_dim_min[1] - text_dim_min[3])), elevationTextMin, font=elevationFont, stroke_width=1)
    shape = [(path_line_coord[currDatapointIndex+1][0], path_line_coord[currDatapointIndex+1][1]), (path_line_coord[currDatapointIndex][0], elevationRect[1][1])]
    draw.line(shape, fill ="white", width = 5)
    draw.rectangle(elevationRect, fill=(255, 255, 255, 127))
    draw.ellipse(xy=[(path_line_coord[currDatapointIndex+1][0] - 5, path_line_coord[currDatapointIndex+1][1] - 5),
                     (path_line_coord[currDatapointIndex+1][0] + 5, path_line_coord[currDatapointIndex+1][1] + 5)],
                 fill=(255, 0, 0), outline=(255, 255, 255), width=2)
def opencv_test(start_frame, gpx_path, style_path, video_path, output_path):
    canvas = CanvasClass.Canvas(video_path, style_path, gpx_path)


    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    interval_in_fps = gpx_item.datapoint_interval * fps
    last_frame = interval_in_fps
    currDatapointIndex = 0
    curr_datapoint = gpx_item.datapoints[currDatapointIndex]
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (frame_width, frame_height))

    frame_counter = 0
    start_time = time.time()

    w = cap.get(3)  # float `width`
    h = cap.get(4)  # float `height`
    path_left_bot_corner_coord = [w * 0.8, h * 0.05]
    path_size = h * 0.3
    frame_time_array = []
    while cap.isOpened():
        # Read the current frame
        ret, frame = cap.read()

        if ret:
            # Process the frame (add number)
            frame_counter += 1
            if frame_counter >= last_frame:
                currDatapointIndex += 1
                curr_datapoint = gpx_item.datapoints[currDatapointIndex]
                last_frame = frame_counter + interval_in_fps
            if frame_counter >= start_frame:
                pil_image = Image.fromarray(frame)
                draw = ImageDraw.Draw(pil_image, "RGBA")
                frame_StartTime = time.time()

                if frame_counter == start_frame:
                    current_time = cap.get(cv2.CAP_PROP_POS_MSEC) / 1000.0
                    print("Current Time:", current_time)
                    cv2.imwrite('./Output/starting_frame.jpg', frame)
                    path_line_coord = gpx_item.get_transformed_gpx_path(path_size, path_left_bot_corner_coord)
                    elevationGraphData = getElevationGraph(w, h, draw, gpx_item.elevation, (0.4, 0.15), (0.5, 0.85))
            # Write the modified frame to the output video



                # Draw non-ascii text onto image
                font = ImageFont.truetype("C:\\Github\\VeloSyncBackEnd\\font\\Oswald-VariableFont_wght.ttf", 35)
                strokeWidth = 2,
                fill_color = (0, 0, 0)
                stroke_color = (255, 255, 255)

                draw.text((50, 80), "Power: "+ str(curr_datapoint.extensions[0].text) + "Watts", font=font, fill=fill_color, stroke_width=1, stroke_fill=stroke_color)
                draw.text((50, 150), "Elevation: "+ str(curr_datapoint.elevation)+"km", font=font, fill=fill_color, stroke_width=1, stroke_fill=stroke_color)
                draw.text((50, 250), "Velocity: "+ str(curr_datapoint.velocity)+"m/s", font=font, fill=fill_color, stroke_width=1, stroke_fill=stroke_color)
                draw.text((50, 350), "Lat: "+ str(curr_datapoint.latitude) + "Long: "+ str(curr_datapoint.longitude), font=font, fill=fill_color, stroke_width=1, stroke_fill=stroke_color)
                draw.line(path_line_coord, fill=(255, 255, 255), width=2)
                draw.ellipse(xy=[(path_line_coord[currDatapointIndex][0] - 5, path_line_coord[currDatapointIndex][1] - 5), (path_line_coord[currDatapointIndex][0] + 5, path_line_coord[currDatapointIndex][1] + 5)], fill=(255, 0, 0), outline=(255, 255, 255), width=2)
                drawElevationGraph(draw, elevationGraphData[0], elevationGraphData[1], elevationGraphData[2], elevationGraphData[3], elevationGraphData[4], elevationGraphData[5], currDatapointIndex)
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
                print('Frame Avg Time:',np.sum(frame_time_array), "/", len(frame_time_array), " = ", np.sum(frame_time_array)/len(frame_time_array))
        else:
            break

    cap.release()
    out.release()
    cv2.destroyAllWindows()

    end_time = time.time()
    elapsed_time = end_time - start_time
    print('Time used:', elapsed_time, 'seconds')


gpx_datapointto_list = GPXUtil.GPXUtils.gpx_datapoint_to_list("FNS_Ride.gpx")
gpx_item = GPXClass.GPXClass("FNS_Ride.gpx")
# velo = list(map(lambda x: x.velocity, gpx_datapointto_list))
# plt.plot(velo)
# plt.show()
# Sample data
# scalar = 5
# displacement = 200

# plt.plot(np.linspace(0, 1, len(gpx_item.elevation)), gpx_item.elevation, label='Array 1')
# plt.show()
# new_plot_coord = gpx_item.get_transformed_gpx_path(20, [100,500])
# new_plot_x, new_plot_y = zip(*new_plot_coord)
# plt.plot(new_plot_x, new_plot_y, label='Array 1')
# plt.show()

video_start_time = "00:26"  # Desired target time in mm:ss format

start_frame = GPXUtil.GPXUtils.find_frame_for_time_in_video('./Video/testing_video.mp4', video_start_time)
start_time = time.time()
opencv_test(start_frame, 'FNS_Ride.gpx', './Style/default.xml', './Video/testing_video.mp4', './Video/output_video.mp4')
end_time = time.time()
elapsed_time = end_time - start_time
print('Time used:', elapsed_time, 'seconds')