import matplotlib.pyplot as plt
import numpy as np
from skimage.io import imread
import FDK as fdk
from skimage.restoration import estimate_sigma
from scipy.ndimage.filters import median_filter



def main():
    param = fdk.param_from_xtekct("/home/sindreno/pa11/testSamplePolyamid3_1fps_gain12.xtekct")

    file_names = [r"radiogram2.tif"]

    for i, file_name in enumerate(file_names):
        print("Processing file nr %i" % i)
        radiogram = imread(r"/home/sindreno/pa11/" + file_name).transpose().astype(np.float64)


        # Half hearted I/I0
        radiogram = radiogram / np.max(radiogram)
        radiogram[:250, :] = 0.95
        radiogram[1800:, :] = 0.95

        print("Sigma before filtering", estimate_sigma(radiogram))
        radiogram = median_filter(radiogram,size=20)

        print("Sigma after filtering", estimate_sigma(radiogram))

        _, center_offset = fdk.find_axis_of_rotation(radiogram, background_internsity=0.95)
        param.center_of_rot_y = center_offset * (
                    param.source_to_object_dist / param.source_to_detector_dist) * param.pixel_size_u

        param.update_calculations()
        #        print("Center offset: %f")%param.object_center_x
        print("Object", param.object_xs.max(), param.object_xs.min())

        Reconimg = fdk.fdk(radiogram, param)

        correct = imread(r"./example_data/AVG_R02_01.tif").transpose().astype(np.float64)



        return Reconimg,correct


Reconimg,correct = main()

plt.imshow(Reconimg)
plt.show()