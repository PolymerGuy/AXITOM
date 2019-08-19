from unittest import TestCase
import numpy as np
from axitom.backprojection import rotate_coordinates

class Test_RotateCoordinates(TestCase):
    def test_rotate_coordinates_90deg(self):
        tol = 1e-9
        n_coordinates = 10
        rotation_angle = np.pi/2.
        xs, ys = np.meshgrid(np.arange(n_coordinates),np.arange(n_coordinates))
        xr,yr = rotate_coordinates(xs,ys,rotation_angle)

        error_xs = np.abs(xr-ys)
        error_ys = np.abs(yr+xs)

        if np.max(error_xs) >tol or np.max(error_ys) >tol:
            print("The maximum error in X after rotation was:",np.max(error_xs) )
            print("The maximum error in Y after rotation was:",np.max(error_ys) )
            self.fail()


    def test_rotate_coordinates_0deg(self):
        tol = 1e-9
        n_coordinates = 10
        rotation_angle = 0.0
        xs, ys = np.meshgrid(np.arange(n_coordinates),np.arange(n_coordinates))
        xr,yr = rotate_coordinates(xs,ys,rotation_angle)

        error_xs = np.abs(xr-xs)
        error_ys = np.abs(yr-ys)

        if np.max(error_xs) >tol or np.max(error_ys) >tol:
            print("The maximum error in X after rotation was:",np.max(error_xs) )
            print("The maximum error in Y after rotation was:",np.max(error_ys) )
            self.fail()

    def test_rotate_coordinates_forward_and_reverse(self):
        tol = 1e-9
        n_coordinates = 10
        rotation_angle = np.pi/4
        xs, ys = np.meshgrid(np.arange(n_coordinates),np.arange(n_coordinates))
        xr_forw,yr_forw = rotate_coordinates(xs,ys,rotation_angle)
        xr,yr = rotate_coordinates(xr_forw,yr_forw,-rotation_angle)


        error_xs = np.abs(xr-xs)
        error_ys = np.abs(yr-ys)

        if np.max(error_xs) >tol or np.max(error_ys) >tol:
            print("The maximum error in X after rotation was:",np.max(error_xs) )
            print("The maximum error in Y after rotation was:",np.max(error_ys) )
            self.fail()

