from unittest import TestCase
from FDK.param import param_from_xtekct
from FDK.parse import parse_xtekct_file
from FDK.phantoms import barrel
from FDK.projection import axis_sym_projection
import numpy as np
import matplotlib.pyplot as plt
import os

from FDK.backprojection import fdk


def main():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    inputfile = parse_xtekct_file(dir_path +  "/example_data/radiogram.xtekct")
    param = param_from_xtekct(inputfile)
    param.n_voxels_x = 50
    param.n_voxels_y = 50
    param.n_voxels_z = 50

    param.object_size_x = 50.
    param.object_size_y = 50.
    param.object_size_z = 50.

    param.n_pixels_u = 50
    param.n_pixels_v = 50

    param.detector_size_u = 50.*4
    param.detector_size_v = 50.*4



    param.source_to_detector_dist = 1.e10
    param.source_to_object_dist = 1.e10

    param.update_calculations()

    print(param.detector_us)


    volume = barrel(100)

    angles = np.array([0.])

    proj = axis_sym_projection(volume, param, angles=angles)

    #plt.imshow(proj)
    #plt.show()


main()

class TestAxis_sym_projection(TestCase):
    # For a parallel beam, the radon transform is just the sum of values along an axis.
    # We can mimic this by setting the source to specimen and source to detector distances equal and very large.

    def test_axis_sym_projection(self):
        #self.fail()
        pass
