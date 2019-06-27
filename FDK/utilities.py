import numpy as np


def find_axis_of_rotation(radiogram,background_internsity = 0.9):
    n,m = np.shape(radiogram)
    xs,ys = np.meshgrid(np.arange(m),np.arange(n))
    covered_pixels = np.zeros_like(radiogram)
    covered_pixels[radiogram<background_internsity] = 1.

    cx = np.average(np.sum(xs * covered_pixels,axis=1)/np.sum(covered_pixels,axis=1))-m/2.
    cy = np.average(np.sum(ys * covered_pixels,axis=0)/np.sum(covered_pixels,axis=0))-n/2.
    return cx,cy




def rotate_coordinates(xs_array, ys_array, angle_rad):
    rx = (xs_array * np.cos(angle_rad) + ys_array * np.sin(angle_rad))
    ry = (-xs_array * np.sin(angle_rad) + ys_array * np.cos(angle_rad))
    return rx, ry
