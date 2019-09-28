import numpy as np

""" Phantoms

This module contains the phantoms that can be used for forward projection and virtual experiments

"""

def barrel(domain_size=128, outer_rad_fraction=0.7,center_val=None):
    """ Barrel shaped phantom with a linear density gradient
    The domain size is cubic with dimension "domain_size" along each axis

    Parameters
    ----------
    domain_size : int
        The length of the sides of the domain
    outer_rad_fraction : float
        The diameter of the barrel given as a the fraction of the side length
    center_val : float
        The density value in the center of the barrel

    Returns
    -------
    ndarray
        The phantom
    """

    center = domain_size / 2.
    domain = np.zeros((domain_size, domain_size, domain_size), dtype=np.float64)
    xs, ys = np.meshgrid(np.arange(domain_size), np.arange(domain_size))
    xs = xs - center
    ys = ys - center
    r = np.sqrt(xs ** 2. + ys ** 2.)
    domain[r < outer_rad_fraction * center, :] = 1.
    if center_val is not None:
        domain = domain * (center_val + (r / (outer_rad_fraction * center)) ** 2. * 0.5)[:, :, np.newaxis]
    return domain



