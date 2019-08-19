from unittest import TestCase
from axitom.phantoms import barrel
from axitom.projection import axis_sym_projection
import numpy as np
import os
import axitom



class TestAxis_sym_projection(TestCase):
    """
    For a parallel beam, the radon transform is just the sum of values along an axis.
    We can mimic this by setting the source to specimen and source to detector distances equal and very large.
    """
    def test_axis_sym_projection(self):
        tol = 1e-6

        dir_path = os.path.dirname(os.path.realpath(__file__))
        param = axitom.config_from_xtekct(dir_path + "/example_data/settings.xtekct")
        param.n_voxels_x = 100
        param.n_voxels_y = 100
        param.n_voxels_z = 100
        #
        param.object_size_x = 100.
        param.object_size_y = 100.
        param.object_size_z = 100.

        param.n_pixels_u = 100
        param.n_pixels_v = 100

        param.detector_size_u = param.object_size_x
        param.detector_size_v = param.object_size_y

        param.source_to_detector_dist = 1.0e20
        param.source_to_object_dist = 1.e20

        param.update()

        volume = barrel(100)

        angles = [0.]

        proj = axis_sym_projection(volume, param, angles=angles)

        error = np.abs(np.sum(volume, axis=1) - proj)

        if np.max(error)>tol:
            self.fail()
