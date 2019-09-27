import numpy as np
from .parse import parse_xtekct_file


class Config(object):

    def __init__(self, n_pixels_u, n_pixels_v, detector_size_u, detector_size_v, source_to_detector_dist,
                 source_to_object_dist, angular_inc=1, center_of_rot=0, **kwargs):
        """ Configuration object which contains all settings neccessary for the forward projection
            and tomographic reconstruction using the axitom algorithm.

        """

        self.n_pixels_u = n_pixels_u
        self.n_pixels_v = n_pixels_v

        self.detector_size_u = detector_size_u
        self.detector_size_v = detector_size_v
        self.source_to_detector_dist = source_to_detector_dist
        self.source_to_object_dist = source_to_object_dist
        self.angular_inc = angular_inc

        self.center_of_rot_u = center_of_rot  # Should be in pixels!

        self.projection_angs = np.arange(0., 360, self.angular_inc)
        self.n_projections = len(self.projection_angs)

        self.object_size_x = self.detector_size_u * self.source_to_object_dist / self.source_to_detector_dist
        self.object_size_y = self.detector_size_u * self.source_to_object_dist / self.source_to_detector_dist
        self.object_size_z = self.detector_size_v * self.source_to_object_dist / self.source_to_detector_dist

        self.voxel_size_x = self.object_size_x / self.n_pixels_u
        self.voxel_size_y = self.object_size_y / self.n_pixels_u
        self.voxel_size_z = self.object_size_z / self.n_pixels_v

        self.pixel_size_u = self.detector_size_u / self.n_pixels_u
        self.pixel_size_v = self.detector_size_v / self.n_pixels_v

        self.center_of_rot_y = self.center_of_rot_u * (
                self.source_to_object_dist / self.source_to_detector_dist) * self.pixel_size_u

        self.object_ys = (np.linspace(0, self.n_pixels_u, self.n_pixels_u,
                                      dtype=np.float64) - self.n_pixels_u / 2.) * self.voxel_size_y
        self.object_xs = (np.linspace(0, self.n_pixels_u, self.n_pixels_u,
                                      dtype=np.float64) - self.n_pixels_u / 2.) * self.voxel_size_x
        self.object_zs = (np.linspace(0, self.n_pixels_v, self.n_pixels_v,
                                      dtype=np.float64) - self.n_pixels_v / 2.) * self.voxel_size_z

        self.detector_us = (np.arange(self.n_pixels_u,
                                      dtype=np.float64) - self.n_pixels_u / 2.) * self.pixel_size_u
        self.detector_vs = (np.arange(self.n_pixels_v,
                                      dtype=np.float64) - self.n_pixels_v / 2.) * self.pixel_size_v

    def with_param(self, **kwargs):
        params = self.__dict__.copy()

        for arg, value in kwargs.items():
            params[arg] = value
        return Config(**params)


def config_from_xtekct(file_path):
    """ Make config object from a Nikon X-tek CT input file

        The .xtekct file is parsed and a config file containing all relevant settings is returned.


        Parameters
        ----------
        file_path : str
            The path to the .xtekct file

        Returns
        -------
        obj
            Config object

        """

    inputfile = parse_xtekct_file(file_path)

    try:

        n_pixels_u = inputfile["DetectorPixelsX"]
        n_pixels_v = inputfile["DetectorPixelsY"]
        detector_size_u = inputfile["DetectorPixelSizeX"] * n_pixels_u
        detector_size_v = inputfile["DetectorPixelSizeY"] * n_pixels_v
        source_to_detector_dist = inputfile["SrcToDetector"]
        source_to_object_dist = inputfile["SrcToObject"]

        conf = Config(n_pixels_u=n_pixels_u, n_pixels_v=n_pixels_v, detector_size_u=detector_size_u,
                      detector_size_v=detector_size_v, source_to_detector_dist=source_to_detector_dist,
                      source_to_object_dist=source_to_object_dist)


    except Exception as e:
        raise IOError("Parsing of X-tec file failed with key: ", e)

    return conf
