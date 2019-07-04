import numpy as np
from parse import parse_xtekct_file

class Param(object):

    def __init__(self):
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
        self.roation_dir = -1
        self.angular_inc = 1.

        self.pixel_offset_u = 0
        self.pixel_offset_v = 0

        self.center_of_rot_y = 0.0

        self.projection_angs = np.arange(0., 360, self.angular_inc) * self.roation_dir
        self.n_projections = len(self.projection_angs)

        self.voxel_size_x = self.object_size_x / self.n_voxels_x
        self.voxel_size_y = self.object_size_y / self.n_voxels_y
        self.voxel_size_z = self.object_size_z / self.n_voxels_z

        self.pixel_size_u = self.detector_size_u / self.n_pixels_u
        self.pixel_size_v = self.detector_size_v / self.n_pixels_v

        self.object_xs = np.linspace(-self.n_voxels_x / 2., self.n_voxels_x / 2., self.n_voxels_x,
                                     dtype=np.float) * self.voxel_size_x
        self.object_ys = np.linspace(-self.n_voxels_y / 2., self.n_voxels_y / 2., self.n_voxels_y,
                                     dtype=np.float) * self.voxel_size_y
        self.object_zs = np.linspace(-self.n_voxels_z / 2., self.n_voxels_z / 2., self.n_voxels_z,
                                     dtype=np.float) * self.voxel_size_z

        self.detector_us = np.linspace(-self.n_pixels_u / 2., self.n_pixels_u / 2., self.n_pixels_u,
                                       dtype=np.float) * self.pixel_size_u + self.pixel_offset_u * self.pixel_size_u
        self.detector_vs = np.linspace(-self.n_pixels_v / 2., self.n_pixels_v / 2., self.n_pixels_v,
                                       dtype=np.float) * self.pixel_size_v + self.pixel_offset_v * self.pixel_size_v

    def update_calculations(self):
        # Calculated

        self.projection_angs = np.arange(0., 360, self.angular_inc) * self.roation_dir
        self.n_projections = len(self.projection_angs)

        self.voxel_size_x = self.object_size_x / self.n_voxels_x
        self.voxel_size_y = self.object_size_y / self.n_voxels_y
        self.voxel_size_z = self.object_size_z / self.n_voxels_z

        self.pixel_size_u = self.detector_size_u / self.n_pixels_u
        self.pixel_size_v = self.detector_size_v / self.n_pixels_v

        self.object_xs = np.linspace(-self.n_voxels_x / 2., self.n_voxels_x / 2., self.n_voxels_x,
                                     dtype=np.float) * self.voxel_size_x
        self.object_ys = np.linspace(-self.n_voxels_y / 2., self.n_voxels_y / 2., self.n_voxels_y,
                                     dtype=np.float) * self.voxel_size_y
        self.object_zs = np.linspace(-self.n_voxels_z / 2., self.n_voxels_z / 2., self.n_voxels_z,
                                     dtype=np.float) * self.voxel_size_z

        self.detector_us = np.linspace(-self.n_pixels_u / 2., self.n_pixels_u / 2., self.n_pixels_u,
                                       dtype=np.float) * self.pixel_size_u + self.pixel_offset_u * self.pixel_size_u
        self.detector_vs = np.linspace(-self.n_pixels_v / 2., self.n_pixels_v / 2., self.n_pixels_v,
                                       dtype=np.float) * self.pixel_size_v + self.pixel_offset_v * self.pixel_size_v




def param_from_xtekct(path):

    inputfile = parse_xtekct_file(path)

    param = Param()

    try:
        param.n_voxels_x = inputfile["VoxelsX"]
        param.n_voxels_y = inputfile["VoxelsY"]
        param.n_voxels_z = inputfile["VoxelsZ"]

        param.object_size_x = inputfile["VoxelSizeX"] * param.n_voxels_x
        param.object_size_y = inputfile["VoxelSizeY"] * param.n_voxels_y
        param.object_size_z = inputfile["VoxelSizeZ"] * param.n_voxels_z

        param.n_pixels_u = inputfile["DetectorPixelsX"]
        param.n_pixels_v = inputfile["DetectorPixelsY"]

        param.detector_size_u = inputfile["DetectorPixelSizeX"] * param.n_pixels_u
        param.detector_size_v = inputfile["DetectorPixelSizeY"] * param.n_pixels_v

        param.source_to_detector_dist = inputfile["SrcToDetector"]
        param.source_to_object_dist = inputfile["SrcToObject"]
    except Exception as e:
        raise IOError("Parsing of X-tec file failed with key: ", e)

    return param