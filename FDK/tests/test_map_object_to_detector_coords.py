from unittest import TestCase

from FDK.config import Config
from FDK.backprojection import map_object_to_detector_coords
import numpy as np
import matplotlib.pyplot as plt


class TestMap_object_to_detector_coords(TestCase):

    def make_default_param(self):
        param = Config()
        param.detector_size_u = param.object_size_x
        param.detector_size_v = param.object_size_y

        param.n_pixels_u = 20
        param.n_pixels_v = 20
        param.n_voxels_x = 20
        param.n_voxels_y = 20
        param.n_voxels_z = 20
        param.update_internals()
        return param


    def test_map_object_to_detector_coords(self):
        # "zero" magnification test
        tol = 1e-6
        # This should yield zero magnification and equal coordinates
        param = self.make_default_param()
        param.source_to_detector_dist = 1.e10
        param.source_to_object_dist = 1.e10
        param.update_internals()



        xs, ys = np.meshgrid(param.object_xs,param.object_ys)
        zs = param.object_zs
        detector_a, detector_b = map_object_to_detector_coords(xs, ys, zs, param)

        corr_us = param.n_pixels_u*(param.detector_us-param.detector_us[0])/param.detector_size_u
        corr_vs = param.n_pixels_v*(param.detector_vs-param.detector_vs[0])/param.detector_size_v

        #TODO: This test is realy nasty! The axes are reversed and its realy hard to reason about the test

        xs_error = np.abs(detector_a[:,:]-corr_us[:,np.newaxis])
        ys_error = np.abs(detector_b[:,:,:].transpose()-corr_vs[:,np.newaxis,np.newaxis])

        if np.max(xs_error)>tol or np.max(ys_error)>tol:
            print(xs_error[:,:])

            self.fail()


    def test_map_object_to_detector_coords_mag(self):
        # "Double" magnification test
        tol = 1e-6
        # This should yield zero magnification and equal coordinates
        param = self.make_default_param()
        param.object_size_x = param.detector_size_u/2
        param.object_size_y = param.detector_size_v/2
        param.object_size_z = param.detector_size_v/2

        param.source_to_detector_dist = 2.e10
        param.source_to_object_dist = 1.e10
        param.update_internals()



        xs, ys = np.meshgrid(param.object_xs,param.object_ys)
        detector_a, detector_b = map_object_to_detector_coords(xs, ys, param.object_zs, param)


        corr_us = param.n_pixels_u*(param.detector_us-param.detector_us[0])/param.detector_size_u
        corr_vs = param.n_pixels_v*(param.detector_vs-param.detector_vs[0])/param.detector_size_v

        #TODO: This test is realy nasty! The axes are reversed and its realy hard to reason about the test

        xs_error = np.abs(detector_a[:,:]-corr_us[:,np.newaxis])
        ys_error = np.abs(detector_b[:,:,:].transpose()-corr_vs[:,np.newaxis,np.newaxis])


        if np.max(xs_error)>tol or np.max(ys_error)>tol:
            print(xs_error)
            self.fail()