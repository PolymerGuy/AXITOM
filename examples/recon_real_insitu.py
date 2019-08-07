from FDK.filtering import ramp_filter_and_weight
from FDK.config import config_from_xtekct
from FDK.backprojection import fdk
import matplotlib.pyplot as plt
import numpy as np
from skimage.io import imread
from FDK.parse import parse_xtekct_file
from FDK.utilities import find_center_of_gravity_in_radiogram
import natsort
from skimage.restoration import estimate_sigma, denoise_bilateral,wiener
from scipy.ndimage.filters import median_filter,gaussian_filter
import os

from imageio import imwrite

def find_images_names(path, file_type=".tif"):
    return natsort.natsorted([file for file in os.listdir(path) if file.endswith(file_type)])

def main():
    inputfile = parse_xtekct_file("/home/sindreno/InSituCt/PVC3/SNO20190503PVC3.xtekct")
    param = config_from_xtekct(inputfile)
    param.axis_sym = True

    file_names = find_images_names("/home/sindreno/InSituCt/PVC3/",".tif")
    file_names = file_names[90:]


    for i,file_name in enumerate(file_names):
        print("Processing file nr %i"%i)
        radiogram = imread("/home/sindreno/InSituCt/PVC3/"+file_name).transpose().astype(np.float64)
        #i +=90

        # Half hearted I/I0
        radiogram = radiogram / np.max(radiogram)
        radiogram[:250,:] = 0.95
        radiogram[1800:,:] = 0.95
        #radiogram[:,1750:] = 0.95
        #radiogram[700:1300,:250] = 0.5
        #radiogram[700:1300,1750:] = 0.5


        #plt.imshow(radiogram)
        #plt.show(block=True)

        print("Sigma before filtering", estimate_sigma(radiogram))
        radiogram = denoise_bilateral(radiogram,sigma_spatial=3, multichannel=False)
        #radiogram = median_filter(radiogram, 20)
        #radiogram = gaussian_filter(radiogram, 20)
        print("Sigma after filtering", estimate_sigma(radiogram))

        roi = radiogram[:,:]
        #plt.imshow(roi)
        #plt.show(block=True)

        _, center_offset = find_center_of_gravity_in_radiogram(roi, background_internsity=0.9)
        param.pixel_offset_u = -center_offset
        param.update()
        print("Center offset: %f")%center_offset


        proj = -np.log(radiogram)[:, :, np.newaxis]



        Reconimg = fdk(proj, param)


        plt.imshow(Reconimg)
        plt.show()
        #imwrite("/home/sindreno/InSituCt/recon3/R02_%i.tif"%int(i),Reconimg[1000:,::-1][:,1:].transpose().astype(np.float32))

        #return Reconimg, proj


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