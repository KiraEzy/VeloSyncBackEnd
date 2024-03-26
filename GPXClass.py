import gpxpy
import numpy as np

import GPXUtil


class GPXClass:
    def __init__(self, GPX_file_path):
        self.GPX_file_path = GPX_file_path

        # general gpx variables
        self.gpx_info = GPXUtil.GPXUtils.extract_gpx_info(GPX_file_path) # this is the general information of the gpx file
        self.datapoint_interval = GPXUtil.GPXUtils.extract_gpx_data_interval(GPX_file_path) # this is the interval between each datapoint
        self.datapoints = GPXUtil.GPXUtils.gpx_datapoint_to_list(GPX_file_path) # this is the list of all the datapoints in the gpx file


        # waypoint variables
        self.latarray = self.gpx_lat_to_list()
        self.lonarray = self.gpx_lon_to_list()
        self.mapped_gpx_path_point_on_scale_long, self.mapped_gpx_path_point_on_scale_lat = self.gpx_to_lat_lon_zero_to_one_mapping()
        # this is two array of lat and lon that represent the gpx path point on the scale of 0 to 1 ( 0,0 is the top left corner and 1,1 is the bottom right corner
        self.mapped_gpx_path_point_on_scale = list(zip(self.mapped_gpx_path_point_on_scale_long, self.mapped_gpx_path_point_on_scale_lat))
        # this is a merged list of lat and lon that represent the gpx path point on the scale of 0 to 1 ( 0,0 is the top left corner and 1,1 is the bottom right corner

        # elevation variables
        self.elevation = self.gpx_elevation_to_list()

    def gpx_elevation_to_list(self):
        elevation = []
        for dp in self.datapoints:
            elevation.append(dp.elevation)
        return elevation
    def gpx_lat_to_list(self):
        lat = []
        for dp in self.datapoints :
            lat.append(dp.latitude)
        return lat

    def gpx_lon_to_list(self):
        lon = []
        for dp in self.datapoints :
            lon.append(dp.longitude)
        return lon

    def gpx_to_lat_lon_zero_to_one_mapping(self):
        longitudes = np.array(self.lonarray)
        latitudes = np.array(self.latarray)
        minLat = np.min(latitudes)
        minLon = np.min(longitudes)
        maxLat = np.max(latitudes)
        maxLon = np.max(longitudes)
        # map all long and lat to 0-1 scale for plotting purposes according to min and max
        mapped_gpx_path_point_on_scale_long = (longitudes - minLon) / (maxLon - minLon)
        mapped_gpx_path_point_on_scale_lat = (latitudes - minLat) / (maxLat - minLat)
        return mapped_gpx_path_point_on_scale_long, mapped_gpx_path_point_on_scale_lat

    def get_transformed_gpx_path(self, scalar, displacement):
        """
        :param scalar: Scale factor such as 100
        :param displacement: Displacement factor such as [100,500]
        :return: An array of tuples of transformed gpx path points, ready for plotting.
        Leftmost point is displacement[0] and bottommost point is displacement[1]
        Rightmost point is displacement[0] + scalar and topmost point is displacement[1] + scalar
        """
        new_plot_x = [(x * scalar) + displacement[0] for x in self.mapped_gpx_path_point_on_scale_long]
        new_plot_y = [(y * scalar) + displacement[1] for y in self.mapped_gpx_path_point_on_scale_lat]
        flipped_y_arr = []
        center_y = sum(new_plot_y) / len(new_plot_y)

        for y in new_plot_y:
            flipped_y = 2 * center_y - y
            flipped_y_arr.append(flipped_y)

        return list(zip(new_plot_x, flipped_y_arr))