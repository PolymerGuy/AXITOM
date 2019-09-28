import numpy as np
from .utilities import _parse_xtekct_file

""" Config object and factory

This module contains the Config class which has all the settings that are used during the reconstruction of the tomogram.
A simple factory for creating Config objects from Nikon XT225ST input files is also provided.

"""




class Config(object):

    def __init__(self, n_pixels_u, n_pixels_v, detector_size_u, detector_size_v, source_to_detector_dist,
                 source_to_object_dist, angular_inc=1, center_of_rot=0, **kwargs):
        """ Configuration object which contains all settings necessary for the forward projection
            and tomographic reconstruction.

        Parameters
        ----------
        n_pixels_u : int
            Number of pixels in the u direction of the sensor
        n_pixels_v : int
            Number of pixels in the u direction of the sensor
        detector_size_u : float
            Detector size in the u direction [mm]
        detector_size_v : float
            Detector size in the u direction [mm]
        source_to_detector_dist : float
            Distance between source and detector [mm]
        source_to_object_dist : float
            Distance between source and object [mm]
        angular_inc : float
            Angular increment used in the reconstruction [deg]
        center_of_rot : float
            Position of the rotation axis in pixels. 0 corresponds to the center of the image

        NOTE: Any non valid arguments are neglected without warning

        """

        self.n_pixels_u = n_pixels_u
        self.n_pixels_v = n_pixels_v

        self.detector_size_u = detector_size_u
        self.detector_size_v = detector_size_v
        self.source_to_detector_dist = source_to_detector_dist
        self.source_to_object_dist = source_to_object_dist
        self.angular_inc = angular_inc

        self.center_of_rot_u = center_of_rot

        # All values below are calculated

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

        self.object_ys = (np.arange(self.n_pixels_u, dtype=np.float64) - self.n_pixels_u / 2.) * self.voxel_size_y
        self.object_xs = (np.arange(self.n_pixels_u, dtype=np.float64) - self.n_pixels_u / 2.) * self.voxel_size_x
        self.object_zs = (np.arange(self.n_pixels_v, dtype=np.float64) - self.n_pixels_v / 2.) * self.voxel_size_z

        self.detector_us = (np.arange(self.n_pixels_u,
                                      dtype=np.float64) - self.n_pixels_u / 2.) * self.pixel_size_u
        self.detector_vs = (np.arange(self.n_pixels_v,
                                      dtype=np.float64) - self.n_pixels_v / 2.) * self.pixel_size_v

    def with_param(self, **kwargs):
        """ Get a clone of the object with the parameter changed and all calculations repeated

            Parameters
            ----------
            kwargs :
                The arguments of the config object that should be changed

            Returns
            -------
            obj
                Config object with new arguments set

            """
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

    inputfile = _parse_xtekct_file(file_path)

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
