import scipy.signal as sig
import numpy as np


def ramp_kernel_real(cutoff, length):
    """Ramp filter kernel in real space defined by the cut-off frequency and the spatial dimension

        Parameters
        ----------
        cutoff : float
            The cut-off frequency
        length : int
            The kernel filter length

        Returns
        -------
        ndarray
            The filter kernel


        """
    pos = np.arange(-length, length, 1)
    return cutoff ** 2.0 * (2.0 * np.sinc(2 * pos * cutoff) - np.sinc(pos * cutoff) ** 2.0)


def add_weights(projections, settings):
    """Add weights to the projections according to the ray length traveled through a voxel

        Parameters
        ----------
        projection : np.ndarray
            The projection used in the reconstruction
        settings : obj
            The settings object containing all necessary settings for the reconstruction

        Returns
        -------
        ndarray
            The projections weighted by the ray length


        """
    uu, vv = np.meshgrid(settings.detector_us, settings.detector_vs)

    weights = settings.source_to_detector_dist / np.sqrt(
        settings.source_to_detector_dist ** 2. + uu ** 2. + vv ** 2.)

    return projections * weights[:, :, np.newaxis]


def ramp_filter_and_weight(projections, settings):
    """Add weights to the projections and apply a ramp-high-pass filter set to 0.5*Nyquist_frequency

        Parameters
        ----------
        projection : np.ndarray
            The projection used in the reconstruction
        settings : obj
            The settings object containing all necessary settings for the reconstruction

        Returns
        -------
        ndarray
            The projections weighted by the ray length and filtered by ramp filter

        """
    projections_weighted = add_weights(projections, settings)

    n_pixels_u, _, _ = np.shape(projections_weighted)
    ramp_kernel = ramp_kernel_real(0.5, n_pixels_u)

    projections_filtered = np.zeros_like(projections_weighted)

    _, n_lines, n_projections = projections_weighted.shape

    for i in range(n_projections):
        for j in range(n_lines):
            projections_filtered[:, j, i] = sig.fftconvolve(projections_weighted[:, j, i], ramp_kernel, mode='same')

    scale_factor = 1. / settings.pixel_size_u * np.pi * (
            settings.source_to_detector_dist / settings.source_to_object_dist)

    return projections_filtered * scale_factor
