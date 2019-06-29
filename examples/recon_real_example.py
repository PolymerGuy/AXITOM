import matplotlib.pyplot as plt
import numpy as np
from skimage.io import imread
import FDK as fdk
from skimage.restoration import estimate_sigma
from scipy.ndimage.filters import median_filter



def main():
    inputfile = fdk.parse_xtekct_file("./example_data/R02_01.xtekct")
    param = fdk.param_from_xtekct(inputfile)
    param.axis_sym = True

    file_names = [r"R02_01.tif"]

    for i, file_name in enumerate(file_names):
        print("Processing file nr %i" % i)
        radiogram = imread(r"./example_data/" + file_name).transpose().astype(np.float64)

        # Half hearted I/I0
        radiogram = radiogram / np.max(radiogram)
        radiogram[:250, :] = 0.95
        radiogram[1800:, :] = 0.95

        print("Sigma before filtering", estimate_sigma(radiogram))
        radiogram = median_filter(radiogram,size=20)

        print("Sigma after filtering", estimate_sigma(radiogram))

        _, center_offset = fdk.find_axis_of_rotation(radiogram, background_internsity=0.9)
        param.center_of_rot_y = center_offset * (
                    param.source_to_object_dist / param.source_to_detector_dist) * param.pixel_size_u

        param.update_calculations()
        #        print("Center offset: %f")%param.object_center_x
        print("Object", param.object_xs.max(), param.object_xs.min())

        Reconimg = fdk.fdk(radiogram, param)

        correct = imread(r"./example_data/AVG_R02_01.tif").transpose().astype(np.float64)



        return Reconimg,correct


Reconimg,correct = main()


def normalize_grey_scales(image):
    undeformed_grey_scale = np.average(image[250:500,0:250])
    background_grey_scale = np.average(image[870:1020,280:375])

    return (image-background_grey_scale)/(undeformed_grey_scale-background_grey_scale)



Reconimg_crop = Reconimg.transpose()[:,::-1][1:,:400]

# plt.imshow(Reconimg.transpose(), cmap=plt.cm.magma)
# plt.clim(vmin=0.0, vmax=0.045)
# plt.figure()
# plt.imshow(correct.transpose(), cmap=plt.cm.magma)

Reconimg_crop_norm = normalize_grey_scales(Reconimg_crop)
correct_norm = normalize_grey_scales(correct.transpose())






plt.figure()
plt.subplot(1, 3, 1)
plt.title("Nikon CT-PRO")
plt.imshow(correct_norm,cmap=plt.cm.magma)
plt.axis('off')
plt.clim(vmin=0.5,vmax=1.0)
plt.colorbar()

plt.subplot(1, 3, 2)
plt.title("AXITOM")
plt.imshow(Reconimg_crop_norm[::-1,:],cmap=plt.cm.magma)
plt.axis('off')
plt.clim(vmin=0.5,vmax=1.0)
plt.colorbar()

plt.subplot(1, 3, 3)
plt.title("Absolute deviation")
plt.imshow(np.abs(Reconimg_crop_norm[::-1,:]-correct_norm),cmap=plt.cm.magma)
plt.axis('off')
plt.clim(vmin=0,vmax=0.05)
plt.colorbar()
plt.tight_layout()
plt.show()