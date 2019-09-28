import numpy as np
import axitom
from unittest import TestCase
from scipy.ndimage.filters import median_filter
import os


def run_reconstruction():
    data_path = os.path.dirname(os.path.realpath(__file__))
    config = axitom.config_from_xtekct(data_path + "/example_data/radiogram.xtekct")
    radiogram = axitom.read_image(data_path + "/example_data/radiogram.tif", flat_corrected=True)

    radiogram = median_filter(radiogram, size=21)

    _, center_offset = axitom.find_center_of_rotation(radiogram, background_internsity=0.9)
    config = config.with_param(center_of_rot=center_offset, n_pixels_u=1500)

    reconstruction = axitom.fdk(radiogram, config)

    return reconstruction


def normalize_grey_scales(image):
    reference_grey_scale = np.average(image[250:500, 0:250])
    background_grey_scale = np.average(image[900:1100, 280:375])

    return (image - background_grey_scale) / (reference_grey_scale - background_grey_scale)


class Test_CompareToExternalSoftware(TestCase):
    def test_compare_to_external_software(self):
        """
        Compare the results obtained by using only a single radiogram from a full dataset to the results
        obtained by using the whole dataset and external reconstruction software. The reconstruction by
        the external software is done in advance and only the result is used here.
        """
        dir_path = os.path.dirname(os.path.realpath(__file__))

        self.tol = 2e-2
        recon = run_reconstruction()
        recon_crop = recon.transpose()[:, ::-1][1:, :400]
        recon_crop_norm = normalize_grey_scales(recon_crop)

        correct = axitom.read_image(dir_path + "/example_data/recon_by_external_software.tif")
        correct_norm = normalize_grey_scales(correct.transpose())

        error_field = np.abs(recon_crop_norm[::-1, :] - correct_norm)

        if np.average(error_field) > self.tol:
            self.fail(
                "The reconstruction did not match the reconstruction performed by another software and the error was: %f" % np.average(
                    error_field))
