from FDK.filtering import ramp_filter_and_weight
from FDK.param import param_from_xtekct
from FDK.backprojection import fdk
import matplotlib.pyplot as plt
import numpy as np
from skimage.io import imread
from FDK.parse import parse_xtekct_file
from FDK.utilities import find_axis_of_rotation
import natsort
from skimage.restoration import estimate_sigma, denoise_bilateral, wiener
from skimage.restoration.non_local_means import denoise_nl_means
from scipy.ndimage.filters import median_filter, gaussian_filter
import os

from imageio import imwrite


def find_images_names(path, file_type=".tif"):
    return natsort.natsorted([file for file in os.listdir(path) if file.endswith(file_type)])


def main():
    inputfile = parse_xtekct_file("/home/sindreno/InSituCt/axisymrecon/SNO20160707_R02_01_Cu025.xtekct")
    param = param_from_xtekct(inputfile)
    param.axis_sym = True

    file_names = ["SNO20160707_R02_01_Cu025_0001.tif"]
    sigmas = np.linspace(6, 12., 10)
    # sigmas = [6.]

    print(sigmas)

    patch_kw = dict(patch_size=5,  # 5x5 patches
                    patch_distance=6,  # 13x13 search area
                    multichannel=False)

    for i, file_name in enumerate(file_names):
        for sig in sigmas:
            print("Processing file nr %i" % i)
            radiogram = imread("/home/sindreno/InSituCt/axisymrecon/" + file_name).transpose().astype(np.float64)
            # i +=90

            # Half hearted I/I0
            radiogram = radiogram / np.max(radiogram)
            radiogram[:250, :] = 0.95
            radiogram[1800:, :] = 0.95
            # radiogram[:,1750:] = 0.95
            # radiogram[700:1300,:250] = 0.5
            # radiogram[700:1300,1750:] = 0.5

            # plt.imshow(radiogram)
            # plt.show(block=True)

            sigma_est = np.mean(estimate_sigma(radiogram, multichannel=True))
            print("Sigma before filtering", estimate_sigma(radiogram))
            #radiogram = denoise_bilateral(radiogram, sigma_spatial=sig, sigma_color=0.05, multichannel=False)
            radiogram = median_filter(radiogram, int(sig))
            # radiogram = denoise_nl_means(radiogram, sigma=sig,multichannel=False)
            # radiogram = denoise_nl_means(radiogram, h=sig * sigma_est, fast_mode=False,
            #                            **patch_kw)
            # radiogram = gaussian_filter(radiogram, 2)
            print("Sigma after filtering", estimate_sigma(radiogram))

            roi = radiogram[:, :]
            # plt.imshow(roi)
            # plt.show(block=True)

            _, center_offset = find_axis_of_rotation(roi, background_internsity=0.9)
            param.center_of_rot_x = center_offset * (
                        param.source_to_object_dist / param.source_to_detector_dist) * param.pixel_size_u
            # param.dang = 360./1700.
            param.update_calculations()
            print("Center offset: %f") % center_offset

            proj = -np.log(radiogram)[:, :, np.newaxis]

            # proj_filtered = filter_projections(proj, param)

            Reconimg = fdk(proj, param)
            plt.imshow(Reconimg,vmin=0.025,vmax=0.05)
            plt.show()

            #imwrite("/home/sindreno/InSituCt/axisymrecon/recon/R02_%.4f.tif" % sig,
            #        Reconimg[1000:, ::-1][:, 1:].transpose().astype(np.float32))

        # return Reconimg, proj


main()
#
# plt.imshow(rec,cmap=plt.cm.magma,vmin=0,vmax=0.06)
# plt.show()
#
# #plt.plot(np.average(rec[:, 1030:1040], axis=1))
# #plt.plot(np.average(rec[:, 530:540], axis=1))
#
# #plt.xlim(xmin=500, xmax=1000)
#
# #cropped = rec[1000:1500,:].transpose()
# #plt.imshow(cropped,cmap=plt.cm.gray)
#
# from imageio import imwrite
# #imwrite("temp.tif",cropped.astype(np.float32))
