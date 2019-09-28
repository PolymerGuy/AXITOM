import numpy as np
import axitom
from axitom.phantoms import barrel
from unittest import TestCase
import os


class Test_SimulatedProjections(TestCase):

    def run_reconstruction_and_compare(self, path_to_projections, correct_body):
        # Set the work path as the filepath to this file
        dir_path = os.path.dirname(os.path.realpath(__file__))

        # Set the same settings as used in the forward projection
        config = axitom.config_from_xtekct(dir_path + "/example_data/settings.xtekct")
        config = config.with_param(n_pixels_u=500, n_pixels_v=500)

        proj = np.load(dir_path + path_to_projections)
        proj = np.exp(-proj)

        reconstruction = axitom.fdk(proj, config)

        # Note that the reconstruction give the radial slice only
        deviation_field = np.abs(correct_body[:250, 250, :] - reconstruction)

        # Sample some deviation values from the background and the interior
        background_deviation = deviation_field[5:60, 75:-75]
        interior_deviation = deviation_field[90:, 75:-75]

        if np.max(background_deviation) > self.tol:
            self.fail("The background was not reconstructed properly with largest deviation of %f" % np.max(
                background_deviation))

        if np.max(interior_deviation) > self.tol:
            self.fail(
                "The interior was not reconstructed properly with largest deviation of %f" % np.max(interior_deviation))

    def test_reconstruction_of_massive_barrel(self):
        """
        Check if the reconstruction of a massive barrel matches the volume model from which
        the radiograms were produced.
        """

        self.tol = 2e-2
        path_to_projections = r"/example_data/barrel_projections_axisym.npy"
        correct = barrel(500)
        self.run_reconstruction_and_compare(path_to_projections, correct)

    def test_reconstruction_of_gradient_barrel(self):
        """
        Check if the reconstruction of a barrel with a radial density gradient matches the volume model from which
        the radiograms were produced.
        """
        self.tol = 2e-2
        path_to_projections = r"/example_data/barrel_grad_projections_axisym.npy"
        correct = barrel(500, center_val=0.5)
        self.run_reconstruction_and_compare(path_to_projections, correct)
