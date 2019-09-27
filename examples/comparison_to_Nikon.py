# Change current work path to aid relative imports of data
import sys
from os.path import join, abspath

sys.path.extend([abspath(".")])

import matplotlib.pyplot as plt
import numpy as np
import axitom
from scipy.ndimage.filters import median_filter

path_to_data = "./axitom/tests/example_data/"

"""
This example reconstructs a tomogram from a single radiogram acquired by a Nikon XT-225st of axis-symmetric body.
The results are then compared to the full tomogram reconstructed using NIKON CT-Pro.

For easier comparison, a small normalization routine is used on the resulting tomogram.
"""


def normalize_grey_scales(image):
    reference_grey_scale = np.average(image[250:500, 0:250])
    background_grey_scale = np.average(image[900:1100, 280:375])

    return (image - background_grey_scale) / (reference_grey_scale - background_grey_scale)


def reconstruct_tomogram():
    config = axitom.config_from_xtekct(join(path_to_data, "radiogram.xtekct"))

    radiogram = axitom.read_image(join(path_to_data, "radiogram.tif"), flat_corrected=True)

    radiogram = median_filter(radiogram, size=41)

#    config = config.with_param(n_pixels_u=1500, detector_size_u=config.detector_size_u * (1500.0 / 2000.))

    _, center_offset = axitom.object_center_of_rotation(radiogram, config, background_internsity=0.9)
    config = config.with_param(center_of_rot=center_offset)

    tomogram = axitom.fdk(radiogram, config)

    return tomogram


recon_tomo = reconstruct_tomogram()

correct = axitom.read_image(join(path_to_data, "recon_by_external_software.tif"))
correct_norm = normalize_grey_scales(correct.transpose())

Reconimg_crop = recon_tomo.transpose()[:, ::-1][1:, :400]
Reconimg_crop_norm = normalize_grey_scales(Reconimg_crop)

plt.figure()
plt.subplot(1, 3, 1)
plt.title("Nikon CT-PRO")
plt.imshow(correct_norm, cmap=plt.cm.magma)
plt.axis('off')
plt.clim(vmin=0.5, vmax=1.0)
plt.colorbar()

plt.subplot(1, 3, 2)
plt.title("AXITOM")
plt.imshow(Reconimg_crop_norm[::-1, :], cmap=plt.cm.magma)
plt.axis('off')
plt.clim(vmin=0.5, vmax=1.0)
plt.colorbar()

plt.subplot(1, 3, 3)
plt.title("Absolute deviation")
plt.imshow(np.abs(Reconimg_crop_norm[::-1, :] - correct_norm), cmap=plt.cm.magma)
plt.axis('off')
plt.clim(vmin=0, vmax=0.05)
plt.colorbar()
plt.tight_layout()
plt.show()
