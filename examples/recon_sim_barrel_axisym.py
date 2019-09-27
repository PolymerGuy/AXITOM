# Change current work path to aid relative imports of data
import sys
from os.path import join, abspath

sys.path.extend([abspath(".")])

import axitom
import numpy as np
from axitom.phantoms import barrel
import matplotlib.pyplot as plt

path_to_data = "./axitom/tests/example_data/"

"""
This example reconstructs a tomogram from a single projection, forward projected using the function fdk.axis_sym_projection.
The tomogram is then compared to the body that was forward projected.
"""


def main():
    config = axitom.config_from_xtekct(join(path_to_data, "sim_barrel.xtekct"))

    radiograms = np.load(join(path_to_data, "proj_barrel.npy"))

    radiograms = np.exp(-radiograms)

    tomogram = axitom.fdk(radiograms, config)

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
