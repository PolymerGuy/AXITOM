import numpy as np
from scipy.ndimage import map_coordinates
from .utilities import rotate_coordinates
from .filtering import ramp_filter_and_weight
from .config import Config


def map_object_to_detector_coords(object_xs, object_ys, object_zs, settings):
    """Map the object coordinates to detector pixel coordinates accounting for cone beam divergence.

        This implementation supports both a axis-symmetric mode and full tomograms.
        This is determined by the shape of the object_xs array.

        The equations and their derivation is found in:
        Turbell, H. (2001). Cone-Beam Reconstruction Using Filtered Backprojection. Science And Technology.
        Retrieved from http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.134.5224&amp;rep=rep1&amp;type=pdf

        Parameters
        ----------
        object_xs : np.ndarray
            The x-coordinate array of the object to be reconstructed
        object_ys : np.ndarray
            The x-coordinate array of the object to be reconstructed
        object_zs : np.ndarray
            The x-coordinate array of the object to be reconstructed
        settings : obj
            The settings object containing all necessary settings for the reconstruction


        Returns
        -------
        detector_cords_a
            The detector coordinates corresponding to the given points
        detector_cords_b
            The detector coordinates corresponding to the given points

        """

    detector_cords_a = (((object_ys * settings.source_to_detector_dist) / (object_xs + settings.source_to_object_dist)) -
          settings.detector_us[0]) / settings.pixel_size_u

    if object_xs.ndim == 2:
        detector_cords_b = (((object_zs[np.newaxis, np.newaxis, :] * settings.source_to_detector_dist) / (
                object_xs[:, :, np.newaxis] + settings.source_to_object_dist)) - settings.detector_vs[
                  0]) / settings.pixel_size_v

    elif object_xs.ndim == 1:
        detector_cords_b = (((object_zs[np.newaxis, :] * settings.source_to_detector_dist) / (
                object_xs[:, np.newaxis] + settings.source_to_object_dist)) - settings.detector_vs[
                  0]) / settings.pixel_size_v
    else:
        raise IOError("Invalid dimensions on the object coordinates")

    return detector_cords_a, detector_cords_b


def fdk_axisym(projection, settings):

    proj_width, proj_height = projection.shape
    proj_center = int(proj_width / 2)

    # Allocate an empty array
    recon_slice = np.zeros((proj_center, proj_height), dtype=np.float)

    for frame_nr, angle in enumerate(settings.projection_angs):
        print("Back projecting frame nr: %i" % frame_nr)

        # Calculate the coordinates of the slice for a given rotation
        x_rotated, y_rotated = rotate_coordinates(np.zeros_like(settings.object_xs)[:proj_center],
                                                  settings.object_ys[:proj_center],
                                                  np.radians(angle))

        # Correct for a center of rotation not being at y=0
        y_rotated += settings.center_of_rot_y

        detector_cords_a, detector_cords_b = map_object_to_detector_coords(x_rotated, y_rotated, settings.object_zs,
                                                                           settings)

        # a is independent of Z but has to match the shape of b
        detector_cords_a = detector_cords_a[:, np.newaxis] * np.ones_like(detector_cords_b)

        # This term is caused by the divergent cone geometry
        ratio = (settings.source_to_object_dist ** 2.) / (settings.source_to_object_dist + x_rotated) ** 2.

        recon_slice = recon_slice + ratio[:, np.newaxis] * map_coordinates(projection,
                                                                           [detector_cords_a, detector_cords_b],
                                                                           cval=0., order=1)

    return recon_slice / np.float(settings.n_projections)


def fdk(projection, param):
    """Filtered back projection algorithm as proposed by Feldkamp David Kress, adapted for axisymmetry.

        This implementation has been adapted for axis-symmetry by using a single projection only and
        by only reconstructing a single R-Z slice.


        This algorithm is based on:
        https://doi.org/10.1364/JOSAA.1.000612

        but follows the notation used by:
        Turbell, H. (2001). Cone-Beam Reconstruction Using Filtered Backprojectionn. Science And Technology.
        Retrieved from http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.134.5224&amp;rep=rep1&amp;type=pdf

        Parameters
        ----------
        projection : np.ndarray
            The projection used in the reconstruction
        settings : obj
            The settings object containing all neccessary settings for the reconstruction


        Returns
        -------
        ndarray
            The reconstructed slice

            The reconstructed slice is a R-Z plane of a axis-symmetric tomogram where Z is the symmetry axis.

        """

    if not isinstance(param, Config):
        raise IOError("Only instances of Param are valid settings")

    if type(projection) != np.ndarray:
        raise IOError("The projections have to be in a numpy ndarray")


    projection = -np.log(projection)

    if projection.ndim == 2:
        projection_filtered = ramp_filter_and_weight(projection[:, :, np.newaxis], param)
    else:
        raise IOError("The projection has to be a 2D array")


    img = fdk_axisym(projection_filtered[:, :, 0], param)
    return img
