import numpy as np
from scipy.ndimage import map_coordinates, rotate
from copy import copy

""" Forward projection routines

This module contains the functions used to forward project a volume onto a sensor plane. These tools are intended for 
virtual experiments, validation and testing. 


"""

def _forward_project(volume, config, angle_deg):
    """ Projection of a volume onto a sensor plane using a conical beam geometry

        Parameters
        ----------
        volume : np.ndarray
            The volume which will be projected onto the sensor
        config : obj
            The settings object
        angle_deg : float
            The angle in degrees that the volume will be rotated before the projection is calculated

        Returns
        -------
        ndarray
            The projection

        """
    data3d = rotate(volume, angle_deg, (1, 0), reshape=False)

    # Now integrate along the rays
    uu, vv = np.meshgrid(config.detector_us, config.detector_vs)

    ratios = (config.object_ys + config.source_to_object_dist) / config.source_to_detector_dist

    pus = (uu[:, np.newaxis, :] * ratios[np.newaxis, :, np.newaxis] - config.object_xs[0]) / config.voxel_size_x
    pvs = (vv[:, np.newaxis, :] * ratios[np.newaxis, :, np.newaxis] - config.object_zs[0]) / config.voxel_size_z
    pys = np.arange(pus.shape[1])[np.newaxis, :, np.newaxis] * np.ones_like(pvs)

    proj2d = np.sum(map_coordinates(data3d[:, :, :], [pvs[:, :, :],
                                                      pys, pus[:, :, :]], cval=0.,order=3), axis=1)

    dist = np.sqrt(config.source_to_detector_dist ** 2. + uu ** 2. + vv ** 2.) / (
        config.source_to_detector_dist) * config.voxel_size_y

    return proj2d * dist


def axis_sym_projection(volume, config, angles=None):
    """ Projection of a volume onto a sensor plane using a conical beam geometry

        This implementation has been adapted for axis-symmetry and returns a single projection only.
        The forward projection is done for several angles and the average projection is returned.

        Parameters
        ----------
        volume : np.ndarray
            The volume which will be projected onto the sensor
        config : obj
            The settings object
        angles : list
            The angles in degrees which will be used for the forward projection

        Returns
        -------
        ndarray
            The projection

        """
    modified_param = copy(config)
    if angles is not None:
        modified_param.projection_angs = angles
        modified_param.nProj = len(modified_param.projection_angs)
    else:
        modified_param.projection_angs = np.linspace(0., 45., config.n_voxels_x / 2)
        modified_param.nProj = len(modified_param.projection_angs)

    projection = np.zeros((config.n_pixels_u, config.n_pixels_v), dtype=np.float)
    for i , angle_deg in  enumerate(modified_param.projection_angs):
        print("Projecting fram nr: ", i)
        projection += _forward_project(volume, modified_param, angle_deg)
    return projection / np.float(modified_param.nProj)
