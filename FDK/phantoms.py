import numpy as np



def barrel(domain_size=128, outer_rad_fraction=0.7):
    center = domain_size / 2.
    domain = np.zeros((domain_size, domain_size, domain_size), dtype=np.float)
    xs, ys = np.meshgrid(np.arange(domain_size), np.arange(domain_size))
    xs = xs - center
    ys = ys - center
    r = np.sqrt(xs ** 2. + ys ** 2.)
    domain[r < outer_rad_fraction * center, :] = 1.
    return domain


def barrel_gradient(domain_size=128, outer_rad_fraction=0.7, center_val=0.5):
    center = domain_size / 2.
    domain = np.zeros((domain_size, domain_size, domain_size), dtype=np.float)
    xs, ys = np.meshgrid(np.arange(domain_size), np.arange(domain_size))
    xs = xs - center
    ys = ys - center
    r = np.sqrt(xs ** 2. + ys ** 2.)
    domain[r < outer_rad_fraction * center, :] = 1.
    domain = domain * (center_val + (r / (outer_rad_fraction * center)) ** 2. * 0.5)[:, :, np.newaxis]
    return domain
