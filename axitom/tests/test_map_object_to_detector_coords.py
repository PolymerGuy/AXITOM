from unittest import TestCase
from axitom.config import Config
from axitom.backprojection import map_object_to_detector_coords
import numpy as np


class TestMap_object_to_detector_coords(TestCase):

    def test_map_object_to_detector_coords_1xmag(self):
        """
        When the detector and object are located at the same distance from the source,
        the magnification should be 1x and the coordinates should be identical.
        """
        # "zero" magnification test
        tol = 1e-6
        # This should yield zero magnification and equal coordinates
        config = Config(n_pixels_u=20, n_pixels_v=20, detector_size_u=200., detector_size_v=200.,
                        source_to_detector_dist=1.e10, source_to_object_dist=1.e10)

        xs, ys = np.meshgrid(config.object_xs, config.object_ys)
        zs = config.object_zs
        detector_a, detector_b = map_object_to_detector_coords(xs, ys, zs, config)

        corr_us = config.n_pixels_u * (config.detector_us - config.detector_us[0]) / config.detector_size_u
        corr_vs = config.n_pixels_v * (config.detector_vs - config.detector_vs[0]) / config.detector_size_v

        xs_error = np.abs(detector_a[:, :] - corr_us[:, np.newaxis])

        ys_error = np.abs(detector_b[:, :, :].transpose() - corr_vs[:, np.newaxis, np.newaxis])

        if np.max(xs_error) > tol or np.max(ys_error) > tol:
            print("Largest error: ", xs_error.max())
            print("at positions: ", np.argmax(xs_error))

            print("Largest error: ", ys_error.max())
            print("at positions: ", np.argmax(ys_error))

            self.fail()

    def test_map_object_to_detector_coords_2xmag(self):
        """
        When the source to detector distance is twice the source to object distance,
        the magnification should be 2x.
        """
        tol = 1e-6
        config = Config(n_pixels_u=20, n_pixels_v=20, detector_size_u=200., detector_size_v=200.,
                        source_to_detector_dist=2.e10, source_to_object_dist=1.e10)

        xs, ys = np.meshgrid(config.object_xs, config.object_ys)
        detector_a, detector_b = map_object_to_detector_coords(xs, ys, config.object_zs, config)

        corr_us = config.n_pixels_u * (config.detector_us - config.detector_us[0]) / config.detector_size_u
        corr_vs = config.n_pixels_v * (config.detector_vs - config.detector_vs[0]) / config.detector_size_v

        xs_error = np.abs(detector_a[:, :] - corr_us[:, np.newaxis])
        ys_error = np.abs(detector_b[:, :, :].transpose() - corr_vs[:, np.newaxis, np.newaxis])

        if np.max(xs_error) > tol or np.max(ys_error) > tol:
            # print(xs_error)
            self.fail()
