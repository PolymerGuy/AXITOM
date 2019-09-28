import numpy as np
import natsort
import os
from imageio import imread

""" Utilites

This module contains various utility functions that does not have any other obvious home 

"""


def _parse_xtekct_file(file_path):
    """Parse a X-tec-CT file into a dictionary
    Only = is considered valid separators

        Parameters
        ----------
        file_path : string
            The path to the file to be parsed

        Returns
        -------
        string
            A dictionary containing all key-value pairs found in the X-tec-CT input file
        """
    myvars = {}
    with open(file_path) as myfile:
        for line in myfile:
            name, var = line.partition("=")[::2]
            try:
                if "." in var:
                    myvars[name.strip()] = float(var)
                else:
                    myvars[name.strip()] = int(var)
            except ValueError:
                myvars[name.strip()] = var

    return myvars


def _find_center_of_gravity_in_projection(projection, background_internsity=0.9):
    """ Find axis of rotation in the projection.
        This is done by binarization of the image into object and background
        and determining the center of gravity of the object.

        Parameters
        ----------
        projection : ndarray
            The projection, normalized between 0 and 1
        background_internsity : float
            The background intensity threshold


        Returns
        -------
        float64
            The center of gravity in the u-direction
        float64
            The center of gravity in the v-direction

        """
    m, n = np.shape(projection)

    binary_proj = np.zeros_like(projection, dtype=np.float)
    binary_proj[projection < background_internsity] = 1.

    area_x = np.sum(binary_proj, axis=1)
    area_y = np.sum(binary_proj, axis=0)

    non_zero_rows = np.arange(n)[area_y != 0.]
    non_zero_columns = np.arange(m)[area_x != 0.]

    # Now removing all columns that does not intersect the object
    object_pixels = binary_proj[non_zero_columns, :][:, non_zero_rows]
    area_x = area_x[non_zero_columns]
    area_y = area_y[non_zero_rows]
    xs, ys = np.meshgrid(non_zero_rows, non_zero_columns)

    # Determine center of gravity
    center_of_grav_x = np.average(np.sum(xs * object_pixels, axis=1) / area_x) - n / 2.
    center_of_grav_y = np.average(np.sum(ys * object_pixels, axis=0) / area_y) - m / 2.
    return center_of_grav_x, center_of_grav_y


def find_center_of_rotation(projection, background_internsity=0.9, method="center_of_gravity"):
    """ Find the axis of rotation of the object in the projection

        Parameters
        ----------
        projection : ndarray
            The projection, normalized between 0 and 1
        background_internsity : float
            The background intensity threshold
        method : string
            The background intensity threshold


        Returns
        -------
        float64
            The center of gravity in the v-direction
        float64
            The center of gravity in the u-direction

        """
    if projection.ndim != 2:
        raise ValueError("Invalid projection shape. It has to be a 2d numpy array")

    if method == "center_of_gravity":
        center_v, center_u = _find_center_of_gravity_in_projection(projection, background_internsity)
    else:
        raise ValueError("Invalid method")

    return center_v, center_u


def rotate_coordinates(xs_array, ys_array, angle_rad):
    """ Rotate coordinate arrays by a given angle

        Parameters
        ----------
        xs_array : ndarray
            Two dimensional coordinate array with x-coordinates
        ys_array : ndarray
            Two dimensional coordinate array with y-coordinates
        angle_rad : float
            Rotation angle in radians

        Returns
        -------
        ndarray
            The rotated x-coordinates
        ndarray
            The rotated x-coordinates

        """
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


def shading_correction(projections, flats, darks):
    """ Perform shading correction on a a list of projections based on a list of flat images and list of dark images.

        The correction is: corrected = (projections-dark)/(flat-dark)

        Parameters
        ----------
        projections : list
            A list of projections that will be corrected
        flats : list
            A list of flat images
        darks : list
            A list of dark images


        Returns
        -------
        list
            A list of corrected projections

        """
    flat_avg = np.array(flats)
    flat_avg = np.average(flat_avg, axis=0)

    dark_avg = np.array(darks)
    dark_avg = np.average(dark_avg, axis=0)

    corrected_projections = []
    for projection in projections:
        corrected_projections.append((projection - dark_avg) / (flat_avg - dark_avg))
    return corrected_projections


def read_image(file_path, flat_corrected=False):
    """ Read an image specified by the file_path
        This function always returns a transposed float64 single channel image

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
        image = np.average(image, axis=2)
    if flat_corrected:
        image = image / image.max()
    return np.array(image).transpose()
