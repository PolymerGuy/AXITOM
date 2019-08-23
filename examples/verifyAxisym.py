import matplotlib.pyplot as plt
import numpy as np
import axitom
from scipy.ndimage import shift
from scipy.ndimage.filters import median_filter



print("pipp")
path = "/home/sindreno/InSituCT/radiograms/"
radiogram_names = axitom.list_files_in_folder(path)[:99]

config = axitom.config_from_xtekct(path + "testSamplePVC6_1fps_gain12.xtekct")

print("pipp")

dark = [axitom.read_image(r"/home/sindreno/InSituCT/shades/Dark.tif")]
flat = [axitom.read_image(r"/home/sindreno/InSituCT/shades/Flat.tif")]

offsets_raw = []
errors_raw = []

offsets_filt = []
errors_filt = []

i=0
filtered = [False,True]

for filt in filtered:
    for radiogram_name in radiogram_names:
        i+=1
        radiogram_uncor = [axitom.read_image(path+radiogram_name)]



        radiogram = axitom.shading_correction(radiogram_uncor,flat,dark)[0]
        print("pipp")


        # plt.imshow(radiogram)
        # plt.show()

        # Remove some edges that are in field of view
        radiogram[:250, :] = 0.95
        radiogram[1800:, :] = 0.95



        if filt:
            radiogram = median_filter(radiogram, size=20)

        _, center_offset = axitom.object_center_of_rotation(radiogram, config, background_internsity=0.9)


        config.update()
        print("org",center_offset)

        pix_shift = center_offset / config.voxel_size_y

        shifted = shift(radiogram,(-pix_shift,0),order=3,cval=0.95)




        _, center_offset = axitom.object_center_of_rotation(shifted, config, background_internsity=0.9)
        print("shifted",center_offset)

        # shifted[shifted>0.9] = 0.



        right = shifted[1000:,:]
        left = shifted[:1000,:]

        error = (right-left[::-1,:])
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
ax2.set_ylabel("Standard deviation of error [-]",color="red")
ax2.tick_params('y', colors='red')

plt.tight_layout()

plt.show()



