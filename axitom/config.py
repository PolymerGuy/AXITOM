import numpy as np
from .parse import parse_xtekct_file


class Config(object):

    def __init__(self):
        """ Configuration object which contains all settings neccessary for the forward projection
            and tomographic reconstruction using the axitom algorithm.

        """

        self.n_voxels_x = 2000
        self.n_voxels_y = 2000
        self.n_voxels_z = 2000

        self.object_size_x = 27.229675726
        self.object_size_y = 27.229675726
        self.object_size_z = 27.229675726

        self.n_pixels_u = 2000
        self.n_pixels_v = 2000

        self.detector_size_u = 400.
        self.detector_size_v = 400.
        self.source_to_detector_dist = 1127.464
        self.source_to_object_dist = 76.7511959075928
        self.angular_inc = 1.

        self.pixel_offset_u = 0
        self.pixel_offset_v = 0

        self.center_of_rot_y = 0.0

        self.projection_angs = np.arange(0., 360, self.angular_inc)
        self.n_projections = len(self.projection_angs)

        self.voxel_size_x = self.object_size_x / self.n_voxels_x
        self.voxel_size_y = self.object_size_y / self.n_voxels_y
        self.voxel_size_z = self.object_size_z / self.n_voxels_z

        self.pixel_size_u = self.detector_size_u / self.n_pixels_u
        self.pixel_size_v = self.detector_size_v / self.n_pixels_v

        self.object_xs = (np.arange(self.n_voxels_x, dtype=np.float64) - self.n_voxels_x / 2.) * self.voxel_size_x
        self.object_ys = (np.arange(self.n_voxels_y, dtype=np.float64) - self.n_voxels_y / 2.) * self.voxel_size_y
        self.object_zs = (np.arange(self.n_voxels_z, dtype=np.float64) - self.n_voxels_z / 2.) * self.voxel_size_z

        self.detector_us = (np.arange(self.n_pixels_u,
                                      dtype=np.float64) - self.n_pixels_u / 2.) * self.pixel_size_u + self.pixel_offset_u * self.pixel_size_u
        self.detector_vs = (np.arange(self.n_pixels_v,
                                      dtype=np.float64) - self.n_pixels_v / 2.) * self.pixel_size_v + self.pixel_offset_v * self.pixel_size_v

    def update(self):
        self.projection_angs = np.arange(0., 360, self.angular_inc)
        self.n_projections = len(self.projection_angs)

        self.voxel_size_x = self.object_size_x / self.n_voxels_x
        self.voxel_size_y = self.object_size_y / self.n_voxels_y
        self.voxel_size_z = self.object_size_z / self.n_voxels_z

        self.pixel_size_u = self.detector_size_u / self.n_pixels_u
        self.pixel_size_v = self.detector_size_v / self.n_pixels_v

        self.object_xs = (np.arange(self.n_voxels_x, dtype=np.float64) - self.n_voxels_x / 2.) * self.voxel_size_x
        self.object_ys = (np.arange(self.n_voxels_y, dtype=np.float64) - self.n_voxels_y / 2.) * self.voxel_size_y
        self.object_zs = (np.arange(self.n_voxels_z, dtype=np.float64) - self.n_voxels_z / 2.) * self.voxel_size_z

        self.detector_us = (np.arange(self.n_pixels_u,
                                      dtype=np.float64) - self.n_pixels_u / 2.) * self.pixel_size_u + self.pixel_offset_u * self.pixel_size_u
        self.detector_vs = (np.arange(self.n_pixels_v,
                                      dtype=np.float64) - self.n_pixels_v / 2.) * self.pixel_size_v + self.pixel_offset_v * self.pixel_size_v


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
    conf = Config()

    try:
        conf.n_voxels_x = inputfile["VoxelsX"]
        conf.n_voxels_y = inputfile["VoxelsY"]
        conf.n_voxels_z = inputfile["VoxelsZ"]

        conf.object_size_x = inputfile["VoxelSizeX"] * conf.n_voxels_x
        conf.object_size_y = inputfile["VoxelSizeY"] * conf.n_voxels_y
        conf.object_size_z = inputfile["VoxelSizeZ"] * conf.n_voxels_z

        conf.n_pixels_u = inputfile["DetectorPixelsX"]
        conf.n_pixels_v = inputfile["DetectorPixelsY"]

        conf.detector_size_u = inputfile["DetectorPixelSizeX"] * conf.n_pixels_u
        conf.detector_size_v = inputfile["DetectorPixelSizeY"] * conf.n_pixels_v

        conf.source_to_detector_dist = inputfile["SrcToDetector"]
        conf.source_to_object_dist = inputfile["SrcToObject"]
    except Exception as e:
        raise IOError("Parsing of X-tec file failed with key: ", e)

    return conf
