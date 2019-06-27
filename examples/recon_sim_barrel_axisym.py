from FDK.param import param_from_xtekct
from FDK.backprojection import fdk
import numpy as np
from FDK.parse import parse_xtekct_file
from FDK.phantoms import barrel
import matplotlib.pyplot as plt





def main():
    inputfile = parse_xtekct_file("example_data/radiogram.xtekct")
    param = param_from_xtekct(inputfile)
    param.n_voxels_x = 500
    param.n_voxels_y = 500
    param.n_voxels_z = 500
    param.n_pixels_u = 500
    param.n_pixels_v = 500
    param.update_calculations()

    volume = barrel(500)

    angles = np.linspace(0., 45., 200)
    print(angles)
#    proj = axis_sym_projection(volume,param,angles=angles)

#
    domain = volume
#
    #np.save("proj_barrel",proj)
    proj = np.load("proj_barrel.npy")




    proj = np.exp(-proj)


    Reconimg = fdk(proj, param)

    return Reconimg, proj, domain


rec, proj, domain = main()
plt.imshow(rec)
plt.figure()
# plt.show()
plt.plot(rec[200,:])
plt.plot(rec[:,250])

#plt.plot(rec[2][128,128,:]/rec[2][128,128,128],'--')
#plt.plot(rec[2][:,128,128]/rec[2][128,128,128],'--')
plt.figure()
plt.imshow(np.abs(domain[:250,250,:]-rec))

plt.show()