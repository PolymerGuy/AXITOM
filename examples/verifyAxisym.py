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

first_frame = int((170./1000.) * 101.)
print("First frame is: ",first_frame)
path = "/home/sindreno/InSituCt/PVCForPaper/radiograms/"
radiogram_names = axitom.list_files_in_folder(path)[:]

config = axitom.config_from_xtekct(path + "testSamplePVC6_1fps_gain12.xtekct")

print("pipp")

dark = [axitom.read_image(r"/home/sindreno/InSituCt/PVCForPaper/flatAndDarks/Dark_160kV160uA.tif")]
flat = [axitom.read_image(r"/home/sindreno/InSituCt/PVCForPaper/flatAndDarks/Flat_160kV160uA.tif")]

offsets_raw = []
errors_raw = []

offsets_filt = []
errors_filt = []

angle_raw = []
angle_filtered = []

i=0
filtered = [True]

for filt in filtered:
    for i,radiogram_name in enumerate(radiogram_names):

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
        radiogram = rotate(radiogram, angle, order=3, reshape=False,cval=0.99)
        _, center_offset,_ = axitom.object_center_of_rotation_ang(radiogram[:,:1700], config, background_internsity=0.96)


        print("Center offset on unrotated image: ",center_offset)

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
        #plt.imshow(np.abs(bin_image),vmin=0.003,vmax=0.01,cmap=plt.cm.plasma)
        #plt.imsave("/home/sindreno/InSituCt/PVCForPaper/artefacts/radiogram_error%i.png"%i,  np.abs(bin_image),vmin=0.003,vmax=0.01,cmap=plt.cm.plasma)
        #plt.show()

        error[right>0.9] = np.nan

        if filt:
            errors_filt.append(np.nanstd(error[:700, :1700]))
            offsets_filt.append(pix_shift)
            angle_filtered.append(angle)

        else:
            errors_raw.append(np.nanstd(error[:700, :1700]))
            offsets_raw.append(pix_shift)
            angle_raw.append(angle)








    # tomogram = axitom.fdk(np.array(radiogram), config)
    # plt.imshow(tomogram)
    # plt.show()

plt.close()
fig, ax1 = plt.subplots()
ax1.plot(offsets_raw,  color="black")
ax1.set_xlim(xmin=0)
ax1.set_ylim(ymin=np.min(offsets_raw))
ax1.set_xlabel("Frame [-]")
ax1.tick_params('y')
ax1.set_ylabel("Center axis offset [pix]")

ax2 = ax1.twinx()
ax2.plot(angle_raw, color="red")
ax2.set_ylabel("Center axis angle [deg]",color="red")
ax2.tick_params('y', colors='red')
ax2.set_ylim(ymin=np.min(angle_raw))


plt.tight_layout()

plt.show()



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



