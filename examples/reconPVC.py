from FDK.filtering import ramp_filter_and_weight
from FDK.config import config_from_xtekct
from FDK.backprojection import fdk
import matplotlib.pyplot as plt
import numpy as np
import FDK as fdk
from skimage.io import imread
from FDK.parse import parse_xtekct_file
from FDK.utilities import find_center_of_gravity_in_radiogram

from skimage.restoration import estimate_sigma, denoise_bilateral, wiener
from scipy.ndimage.filters import median_filter, gaussian_filter
import os
from scipy.signal import savgol_filter

from imageio import imwrite


def find_images_names(path, file_type=".tif"):
    return sorted([file for file in os.listdir(path) if file.endswith(file_type)])


def main():
    param = config_from_xtekct("/home/sindreno/InSituCt/PVCForPaper/radiograms/testSamplePVC6_1fps_gain12.xtekct")
    param.axis_sym = True

    file_names = find_images_names("/home/sindreno/InSituCt/PVCForPaper/radiograms/", ".tif")
    #file_names = [file_names[0]]

    flats = fdk.read_image("/home/sindreno/InSituCt/PVCForPaper/flatAndDarks/Flat_160kV160uA.tif", flat_corrected=False)
    darks = fdk.read_image("/home/sindreno/InSituCt/PVCForPaper/flatAndDarks/Dark_160kV160uA.tif", flat_corrected=False)

    sigmas = [4.]
    for sigma in sigmas:
        for i, file_name in enumerate(file_names):
            print("Processing file nr %i with name %s" % (i, file_name))
            radiogram = fdk.read_image("/home/sindreno/InSituCt/PVCForPaper/radiograms/" + file_name,
                                       flat_corrected=False)
            radiogram = fdk.shading_correction([radiogram], [flats], [darks])[0]

            print("Sigma before filtering", estimate_sigma(radiogram))
            # if sigma!=0.:
            #    radiogram = denoise_bilateral(radiogram,sigma_color= 0.8,  sigma_spatial=10, multichannel=False)
            radiogram_median = median_filter(radiogram, 20)
            n,m = radiogram.shape
            for row in range(n):
                radiogram[:,row] = savgol_filter(radiogram[:,row],31,3)


            plt.figure()
            plt.imshow(radiogram_median,cmap=plt.cm.Blues)
            plt.figure()
            plt.imshow(radiogram)
            plt.show()


            # radiogram = gaussian_filter(radiogram, 20)
            print("Sigma after filtering", estimate_sigma(radiogram))


            #imwrite("/home/sindreno/InSituCt/PVCForPaper/tomograms/radio.tif",
            #        radiogram.transpose().astype(np.float32))


            radiogram[:250, :] = 0.99999
            radiogram[1750:, ] = 0.99999

            #radiogram= radiogram[250:1750,:]

            #radiogram_cut = radiogram[:, :1750]

            radiogram_cut = radiogram.copy()[:,:1750]




            # plt.imshow(radiogram_cut.transpose(),cmap=plt.cm.gray)
            # plt.show()

            _, center_offset = find_center_of_gravity_in_radiogram(radiogram_cut, background_internsity=0.95)
            param.pixel_offset_u = -center_offset
            param.angular_inc = 0.5
            param.update()
            print("Center offset: %s", center_offset)

            Reconimg = fdk.fdk(radiogram, param)

            plt.imshow(Reconimg,vmin=0.025,vmax=0.05)
            plt.show()

       #      imwrite("/home/sindreno/InSituCt/PVCForPaper/tomograms/PVC%i.tif" % int(i),
       #              Reconimg[:, 1:].transpose().astype(np.float32))

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
