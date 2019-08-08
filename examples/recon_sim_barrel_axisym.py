import FDK as fdk
import numpy as np
from FDK.phantoms import barrel
import matplotlib.pyplot as plt

"""
This example reconstructs a tomogram from a single projection, forward projected using the function fdk.axis_sym_projection.
The tomogram is then compared to the body that was forward projected.
"""


def main():
    config = fdk.config_from_xtekct("./example_data/radiogram.xtekct")
    config.n_voxels_x = 500
    config.n_voxels_y = 500
    config.n_voxels_z = 500
    config.n_pixels_u = 500
    config.n_pixels_v = 500
    config.update()

    radiograms = np.load("proj_barrel.npy")

    radiograms = np.exp(-radiograms)

    tomogram = fdk.fdk(radiograms, config)

    return tomogram


rec = main().transpose()

correct_norm = barrel(500)[:250, 250, :].transpose()

plt.figure()
plt.subplot(1, 3, 1)
plt.title("Correct")
plt.imshow(correct_norm, cmap=plt.cm.magma)
plt.axis('off')
plt.clim(vmin=0.5, vmax=1.0)
plt.colorbar()

plt.subplot(1, 3, 2)
plt.title("Reconstruction")
plt.imshow(rec[::-1, :], cmap=plt.cm.magma)
plt.axis('off')
plt.clim(vmin=0.5, vmax=1.0)
plt.colorbar()

plt.subplot(1, 3, 3)
plt.title("Absolute deviation")
plt.imshow(np.abs(rec[::-1, :] - correct_norm), cmap=plt.cm.magma)
plt.axis('off')
plt.clim(vmin=0, vmax=0.05)
plt.colorbar()
plt.tight_layout()
plt.show()
