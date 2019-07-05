import numpy as np
import natsort
import os
from imageio import imread


def find_center_of_gravity_in_radiogram(radiogram, background_internsity=0.9):
    """ Find axis of rotation in the radiogram.
        This is done by binarization of the image into object and background
        and determining the center of gravity of the object.

        Parameters
        ----------
        radiogram : ndarray
            The radiogram, normalized between 0 and 1
        background_internsity : float
            The background intensity threshold


        Returns
        -------
        float64
            The center of gravity in the u-direction
        float64
            The center of gravity in the v-direction

        """
    n, m = np.shape(radiogram)
    xs, ys = np.meshgrid(np.arange(m), np.arange(n))
    covered_pixels = np.zeros_like(radiogram,dtype=np.float)
    covered_pixels[radiogram < background_internsity] = 1.

    # Determine center of gravity
    center_of_grav_x = np.average(np.sum(xs * covered_pixels, axis=1) / np.sum(covered_pixels, axis=1)) - m / 2.
    center_of_grav_y = np.average(np.sum(ys * covered_pixels, axis=0) / np.sum(covered_pixels, axis=0)) - n / 2.
    return center_of_grav_x, center_of_grav_y


def object_center_of_rotation(radiogram, param, background_internsity=0.9, method="center_of_gravity"):
    """ Find the axis of rotation of the object pictures in the radiogram
        This is done by determining the center of rotation of the radiogram and scaling the coordinates
        to object coordinates

        Parameters
        ----------
        radiogram : ndarray
            The radiogram, normalized between 0 and 1
        param : object
            The parameters used for the tomographic reconstruction
        background_internsity : float
            The background intensity threshold
        method : string
            The background intensity threshold


        Returns
        -------
        float64
            The center of gravity in the x-direction
        float64
            The center of gravity in the y-direction

        """
    if radiogram.ndim != 2:
        raise ValueError("Invalid radiogram shape. It has to be a 2d numpy array")

    if method == "center_of_gravity":
        center_x,center_y = find_center_of_gravity_in_radiogram(radiogram,background_internsity)
    else:
        raise ValueError("Invalid method")

    scale = (param.source_to_object_dist / param.source_to_detector_dist) * param.pixel_size_u

    return scale * center_x, scale * center_y


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


def read_image(file_path, flat_corrected=False):
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
        image =  np.average(image, axis=2)
    if flat_corrected:
        image = image/image.max()
    return image.transpose()
