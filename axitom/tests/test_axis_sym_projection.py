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
        config = axitom.Config(n_pixels_u=100, n_pixels_v=100, detector_size_u=100., detector_size_v=100.,
                               source_to_detector_dist=1.e20, source_to_object_dist=1.e20)

        volume = barrel(100)

        angles = [0.]

        proj = axis_sym_projection(volume, config, angles=angles)

        error = np.abs(np.sum(volume, axis=1) - proj)

        if np.max(error) > tol:
            self.fail()
