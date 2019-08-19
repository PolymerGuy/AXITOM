import numpy as np
import axitom
from unittest import TestCase
from scipy.ndimage.filters import median_filter
import os


def run_reconstruction():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    config = axitom.config_from_xtekct(dir_path + "/example_data/settings.xtekct")
    radiogram = axitom.read_image(dir_path + "/example_data/radiogram.tif", flat_corrected=True)

    # Remove some edges that are in field of view
    radiogram[:250, :] = 0.95
    radiogram[1800:, :] = 0.95

    radiogram = median_filter(radiogram, size=20)

    _, center_offset = axitom.object_center_of_rotation(radiogram, config, background_internsity=0.9)
    config.center_of_rot_y = center_offset

    config.update()

    reconstruction = axitom.fdk(radiogram, config)

    return reconstruction


def normalize_grey_scales(image):
    undeformed_grey_scale = np.average(image[250:500, 0:250])
    background_grey_scale = np.average(image[870:1020, 280:375])

    return (image - background_grey_scale) / (undeformed_grey_scale - background_grey_scale)


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
