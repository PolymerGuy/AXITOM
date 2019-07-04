import numpy as np
import natsort
import os
from imageio import imread


def find_axis_of_rotation(radiogram, background_internsity=0.9):
    n, m = np.shape(radiogram)
    xs, ys = np.meshgrid(np.arange(m), np.arange(n))
    covered_pixels = np.zeros_like(radiogram)
    covered_pixels[radiogram < background_internsity] = 1.

    cx = np.average(np.sum(xs * covered_pixels, axis=1) / np.sum(covered_pixels, axis=1)) - m / 2.
    cy = np.average(np.sum(ys * covered_pixels, axis=0) / np.sum(covered_pixels, axis=0)) - n / 2.
    return cx, cy


def rotate_coordinates(xs_array, ys_array, angle_rad):
    rx = (xs_array * np.cos(angle_rad) + ys_array * np.sin(angle_rad))
    ry = (-xs_array * np.sin(angle_rad) + ys_array * np.cos(angle_rad))
    return rx, ry


def list_files_in_folder(path, file_type=".tif"):
    """ List all files with a given extension for a given path. The output is sorted

        Parameters
        ----------
        path : str
            Path to the folder containing the files
        file_type : str
            The file extension ex. ".tif"

        Returns
        -------
        list
            A list of sorted file names

        """
    return natsort.natsorted([file for file in os.listdir(path) if file.endswith(file_type)])


def shading_correction(radiograms, flats, darks):
    """ Perform shading correction on a a list of radiograms based on a list of flat images and list of dark images.

        The correction is: corrected = (radiogram-dark)/(flat-dark)

        Parameters
        ----------
        radiograms : list
            A list of radiograms that will be corrected
        flats : list
            A list of flat images
        darks : list
            A list of dark images


        Returns
        -------
        list
            A list of corrected radiograms

        """
    flat_avg = np.array(flats)
    flat_avg = np.average(flat_avg, axis=0)

    dark_avg = np.array(darks)
    dark_avg = np.average(dark_avg, axis=0)

    corrected_radiograms = []
    for radiogram in radiograms:
        corrected_radiograms.append((radiogram - dark_avg) / (flat_avg - dark_avg))
    return corrected_radiograms


def read_image(file_path):
    """ Read an image specified by the file_path
        This function allways returns a float64 single channel image

        Parameters
        ----------
        file_path : str
            Path to the file

        Returns
        -------
        ndarray
            The single channel image with float64 values

        """
    image = imread(file_path).astype(np.float64)
    if image.ndim == 3:
        return np.average(image, axis=2).transpose()
    return image.transpose()
