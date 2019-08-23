import matplotlib.pyplot as plt
import numpy as np
import axitom
from scipy.ndimage import shift
from scipy.ndimage.filters import median_filter



print("pipp")
path = "/home/sindreno/artefacts/noise/radios/"
radiogram_names = axitom.list_files_in_folder(path,file_type=".tif")[:-10]
print(radiogram_names)


print("pipp")

dark = [axitom.read_image(r"/home/sindreno/artefacts/noise/shades/Dark.tif")]
flat = [axitom.read_image(r"/home/sindreno/artefacts/noise/shades/Flat.tif")]

offsets = []
errors = []
radiogram_uncor = [axitom.read_image(path+radiogram_name) for radiogram_name in radiogram_names]


radiograms = np.array(axitom.shading_correction(radiogram_uncor,flat,dark))[:,250:1750,:]
vmax= 0.343
vmin = 0.22

#radiograms = (radiograms-vmin)/(vmax-vmin)



avg = np.average(radiograms,axis=0)
std = np.std(radiograms,axis=0)
cv = std/avg

specimen = np.zeros_like(avg,dtype=np.bool)
specimen[avg<0.90] = 1


save = "/home/sindreno/artefacts/"


plt.figure()
plt.imshow(avg.transpose(),cmap=plt.cm.plasma)
plt.colorbar(orientation="horizontal",shrink=0.5,pad=0.05)
plt.axis('off')
plt.tight_layout()
plt.savefig(save+"avg_radio.pdf",pad_inches=0,bbox_inches="tight")
plt.close()


plt.figure()
plt.imshow(std.transpose(),cmap=plt.cm.plasma)
plt.colorbar(orientation="horizontal",shrink=0.5,pad=0.05)
plt.axis('off')
plt.tight_layout()
plt.savefig(save+"std_radio.pdf",pad_inches=0,bbox_inches="tight")
plt.close()



plt.figure()
plt.imshow(cv.transpose(),cmap=plt.cm.plasma)
plt.colorbar(orientation="horizontal",shrink=0.5,pad=0.05)
plt.axis('off')
plt.tight_layout()
plt.savefig(save+"cv_radio.pdf",pad_inches=0,bbox_inches="tight")
plt.close()

print("Average standard deviation = ",np.average(std[specimen]))

plt.show()

plt.imshow(specimen.astype(np.int))
plt.show()


    #plt.imshow(error)
    #plt.show()





    # tomogram = axitom.fdk(np.array(radiogram), config)
    # plt.imshow(tomogram)
    # plt.show()




