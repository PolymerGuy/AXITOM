import numpy as np
import FDK as fdk
from FDK.phantoms import barrel, barrel_gradient
from unittest import TestCase

import matplotlib.pyplot as plt

from skimage.restoration import estimate_sigma
from scipy.ndimage.filters import median_filter
from skimage.io import imread
import os


def main():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    inputfile = fdk.parse_xtekct_file(dir_path +  "/example_data/radiogram.xtekct")
    param = fdk.param_from_xtekct(inputfile)
    param.axis_sym = True

    file_names = [r"./example_data/R02_01.tif"]

    for i, file_name in enumerate(file_names):
        print("Processing file nr %i" % i)
        radiogram = imread(dir_path + "/example_data/R02_01.tif").transpose().astype(np.float64)

        # Half hearted I/I0
        radiogram = radiogram / np.max(radiogram)
        radiogram[:250, :] = 0.95
        radiogram[1800:, :] = 0.95

        print("Sigma before filtering", estimate_sigma(radiogram))
        radiogram = median_filter(radiogram,size=20)

        print("Sigma after filtering", estimate_sigma(radiogram))

        _, center_offset = fdk.find_axis_of_rotation(radiogram, background_internsity=0.9)
        param.center_of_rot_y = center_offset * (
                    param.source_to_object_dist / param.source_to_detector_dist) * param.pixel_size_u

        param.update_calculations()
        #        print("Center offset: %f")%param.object_center_x
        print("Object", param.object_xs.max(), param.object_xs.min())

        Reconimg = fdk.fdk(radiogram, param)




        return Reconimg




def normalize_grey_scales(image):
    undeformed_grey_scale = np.average(image[250:500,0:250])
    background_grey_scale = np.average(image[870:1020,280:375])

    return (image-background_grey_scale)/(undeformed_grey_scale-background_grey_scale)




class Test_real_FDK(TestCase):
    def test_backprojection_of_tensile_specimen(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))

        self.tol = 2e-2
        Reconimg = main()
        Reconimg_crop = Reconimg.transpose()[:, ::-1][1:, :400]
        Reconimg_crop_norm = normalize_grey_scales(Reconimg_crop)

        correct = imread(dir_path + "/example_data/AVG_R02_01.tif").transpose().astype(np.float64)
        correct_norm = normalize_grey_scales(correct.transpose())


        error_field = np.abs(Reconimg_crop_norm[::-1,:]-correct_norm)


        if np.average(error_field) > self.tol:
            self.fail("The reconstruction did not match the reconstruction performed by another software and the error was: %f" % np.average(
                error_field))

