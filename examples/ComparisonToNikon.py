import matplotlib.pyplot as plt
import numpy as np
import FDK as fdk
from scipy.ndimage.filters import median_filter


def normalize_grey_scales(image):
    reference_grey_scale = np.average(image[250:500, 0:250])
    background_grey_scale = np.average(image[870:1020, 280:375])

    return (image - background_grey_scale) / (reference_grey_scale - background_grey_scale)


def main():
    config = fdk.config_from_xtekct("./example_data/R02_01.xtekct")
    file_names = [r"R02_01.tif"]

    for i, file_name in enumerate(file_names):
        print("Processing file nr %i" % i)
        radiogram = fdk.read_image(r"./example_data/" + file_name, flat_corrected=True)

        # Remove some edges that are in field of view
        radiogram[:250, :] = 0.95
        radiogram[1800:, :] = 0.95

        radiogram = median_filter(radiogram, size=20)

        _, center_offset = fdk.object_center_of_rotation(radiogram, config, background_internsity=0.9)
        config.center_of_rot_y = center_offset

        config.update_internals()

        tomo = fdk.fdk(radiogram, config)

        return tomo


recon = main()

correct = fdk.read_image(r"./example_data/AVG_R02_01.tif")
correct_norm = normalize_grey_scales(correct.transpose())


Reconimg_crop = recon.transpose()[:, ::-1][1:, :400]
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
