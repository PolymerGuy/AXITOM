import numpy as np
import FDK as fdk
from FDK.phantoms import barrel
from unittest import TestCase
import os

def run_backprojection_full():
    dir_path = os.path.dirname(os.path.realpath(__file__))

    param = fdk.config_from_xtekct(dir_path + "/example_data/radiogram.xtekct")
    param.axis_sym = True
    param.n_voxels_x = 500
    param.n_voxels_y = 500
    param.n_voxels_z = 500
    param.n_pixels_u = 500
    param.n_pixels_v = 500
    param.update_internals()

    domain = barrel(500)

    proj = np.load(dir_path + "/example_data/barrel_projections_axisym.npy")

    proj = np.exp(-proj)

    Reconimg = fdk.fdk(proj, param)

    return Reconimg, proj, domain


def run_backprojection_hollow():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    param = fdk.config_from_xtekct(dir_path +"/example_data/radiogram.xtekct")
    param.axis_sym = True
    param.n_voxels_x = 500
    param.n_voxels_y = 500
    param.n_voxels_z = 500
    param.n_pixels_u = 500
    param.n_pixels_v = 500
    param.update_internals()

    domain = barrel(500,center_val=0.5)

    proj = np.load(dir_path + "/example_data/barrel_grad_projections_axisym.npy")

    proj = np.exp(-proj)

    Reconimg = fdk.fdk(proj, param)

    return Reconimg, proj, domain

class Test_simulated_FDK(TestCase):
    def test_backprojection_of_massive_barrel(self):
        self.tol = 2e-2
        rec, proj, domain = run_backprojection_full()
        deviation_field = np.abs(domain[:250, 250, :] - rec)

        background_deviation = deviation_field[5:60, 75:-75]
        interior_deviation = deviation_field[90:, 75:-75]

        if np.max(background_deviation) > self.tol:
            self.fail("The background was not reconstructed properly with largers deviation of %f" % np.max(
                background_deviation))

        if np.max(interior_deviation) > self.tol:
            self.fail(
                "The interior was not reconstructed properly with largers deviation of %f" % np.max(interior_deviation))

    def test_backprojection_of_gradient_barrel(self):
        self.tol = 2e-2
        rec, proj, domain = run_backprojection_hollow()
        deviation_field = np.abs(domain[:250, 250, :] - rec)

        background_deviation = deviation_field[5:60, 75:-75]
        interior_deviation = deviation_field[90:, 75:-75]

        if np.max(background_deviation) > self.tol:
            self.fail("The background was not reconstructed properly with largers deviation of %f" % np.max(
                background_deviation))

        if np.max(interior_deviation) > self.tol:
            self.fail(
                "The interior was not reconstructed properly with largers deviation of %f" % np.max(interior_deviation))
