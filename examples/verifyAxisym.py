import matplotlib.pyplot as plt
import numpy as np
import axitom
from scipy.ndimage import shift
from scipy.ndimage.filters import median_filter

from scipy.ndimage import rotate

def rebin(arr, new_shape):
    """Rebin 2D array arr to shape new_shape by averaging."""
    shape = (new_shape[0], arr.shape[0] // new_shape[0],
             new_shape[1], arr.shape[1] // new_shape[1])
    return arr.reshape(shape).mean(-1).mean(1)

print("pipp")
path = "/home/sindreno/InSituCT/radiograms/"
radiogram_names = axitom.list_files_in_folder(path)[99:]

config = axitom.config_from_xtekct(path + "testSamplePVC6_1fps_gain12.xtekct")

print("pipp")

dark = [axitom.read_image(r"/home/sindreno/InSituCT/shades/Dark.tif")]
flat = [axitom.read_image(r"/home/sindreno/InSituCT/shades/Flat.tif")]

offsets_raw = []
errors_raw = []

offsets_filt = []
errors_filt = []

i=0
filtered = [False]

for filt in filtered:
    for radiogram_name in radiogram_names:
        i+=1
        radiogram_uncor = [axitom.read_image(path+radiogram_name)]



        radiogram = axitom.shading_correction(radiogram_uncor,flat,dark)[0]
        print("pipp")


        # plt.imshow(radiogram)
        # plt.show()

        # Remove some edges that are in field of view
        radiogram[:250, :] = 0.99
        radiogram[1800:, :] = 0.99



        if filt:
            radiogram = median_filter(radiogram, size=20)

        _, center_offset,angle = axitom.object_center_of_rotation_ang(radiogram[:,:1700], config, background_internsity=0.96)

        print("Center offset on unrotated image: ",center_offset)

        radiogram = rotate(radiogram, angle, order=3, reshape=False,cval=0.99)
        config.center_of_rot_y = center_offset

        config.update()

#        plt.imshow(radiogram.transpose())
#        plt.show()

#        tomo = axitom.fdk(radiogram,config)
#        plt.imshow(tomo.transpose(),vmin=0.0,vmax=0.06)
#        plt.show()



        pix_shift = center_offset / config.voxel_size_y

        shifted = shift(radiogram,(-pix_shift,0),order=3,cval=0.99)




        _, center_offset,_ = axitom.object_center_of_rotation_ang(shifted, config, background_internsity=0.96)
        print("Center offset on rotated image: ",center_offset)

        # shifted[shifted>0.9] = 0.




        right = shifted[1000:,:]
        left = shifted[:1000,:]

        error = (right-left[::-1,:])

        bin_image = np.abs(error[:700, :]).transpose()
        # print(bin_image.shape)
        bin_image = rebin(bin_image,(500,175))
        plt.imshow(np.abs(bin_image),vmin=0.003,vmax=0.01,cmap=plt.cm.plasma)
        # # plt.imsave("/home/sindreno/artefacts/radiogram_error_80.png",  np.abs(bin_image),vmin=0.0,vmax=0.01,cmap=plt.cm.plasma)
        plt.show()

        error[right>0.9] = np.nan

        if filt:
            errors_filt.append(np.nanmean(error[:700, :1700]))
            offsets_filt.append(pix_shift)
        else:
            errors_raw.append(np.nanmean(error[:700, :1700]))
            offsets_raw.append(pix_shift)








    # tomogram = axitom.fdk(np.array(radiogram), config)
    # plt.imshow(tomogram)
    # plt.show()


plt.close()
fig, ax1 = plt.subplots()
ax1.plot(offsets_raw,  color="black")
ax1.plot(offsets_filt, "--", color="black")
#ax1.set_xlim(xmin=0)
#ax1.set_ylim(ymin=20)
ax1.set_xlabel("Frame [-]")
ax1.tick_params('y')
ax1.set_ylabel("Center axis offset [pix]")

ax2 = ax1.twinx()
ax2.plot(errors_raw, color="red")
ax2.plot(errors_filt, "--", color="red")
ax2.set_ylabel("Average value of error [-]",color="red")
ax2.tick_params('y', colors='red')

plt.tight_layout()

plt.show()



