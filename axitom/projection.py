import numpy as np
from scipy.ndimage import map_coordinates, rotate
from copy import copy


def forward_project(data, param, angle_deg):

    # Rotate the data3d around the third axis

    data3d = rotate(data, angle_deg, (1, 0), reshape=False)

    # Now integrate along the rays
    uu, vv = np.meshgrid(param.detector_us, param.detector_vs)

    Ratios = (param.object_ys + param.source_to_object_dist) / param.source_to_detector_dist

    pus = (uu[:, np.newaxis, :] * Ratios[np.newaxis, :, np.newaxis] - param.object_xs[0]) / param.voxel_size_x
    pvs = (vv[:, np.newaxis, :] * Ratios[np.newaxis, :, np.newaxis] - param.object_zs[0]) / param.voxel_size_z
    pys = np.arange(pus.shape[1])[np.newaxis, :, np.newaxis] * np.ones_like(pvs)

    proj2d = np.sum(map_coordinates(data3d[:, :, :], [pvs[:, :, :],
                                                      pys, pus[:, :, :]], cval=0.,order=3), axis=1)

    dist = np.sqrt(param.source_to_detector_dist ** 2. + uu ** 2. + vv ** 2.) / (
        param.source_to_detector_dist) * param.voxel_size_y

    return proj2d * dist


def axis_sym_projection(volume, param, angles=None):
    """ Projection of a volume onto a sensor plane using a conical beam geometry

        This implementation has been adapted for axis-symmetry and returns a single projection only

        Parameters
        ----------
        volume : np.ndarray
            The volume which will be projected onto the sensor
        param : obj
            The settings object
        angles : list
            The angles which will be used for the forward projection

        Returns
        -------
        ndarray
            The projection

        """
    modified_param = copy(param)
    if angles is not None:
        modified_param.projection_angs = angles
        modified_param.nProj = len(modified_param.projection_angs)
    else:
        modified_param.projection_angs = np.linspace(0., 45., param.n_voxels_x / 2)
        modified_param.nProj = len(modified_param.projection_angs)

    radiogram = np.zeros((param.n_pixels_u, param.n_pixels_v), dtype=np.float)
    for i , angle_deg in  enumerate(modified_param.projection_angs):
        print("Projecting fram nr: ", i)
        radiogram += forward_project(volume, modified_param, angle_deg)
    return radiogram / np.float(modified_param.nProj)
