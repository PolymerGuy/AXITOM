from FDK.param import config_from_xtekct
from FDK.backprojection import fdk
import numpy as np
from FDK.parse import parse_xtekct_file
from FDK.phantoms import barrel_gradient
import matplotlib.pyplot as plt

from skimage.restoration import estimate_sigma



def main():
    inputfile = parse_xtekct_file("example_data/radiogram.xtekct")
    param = config_from_xtekct(inputfile)
    param.axis_sym = True
    param.n_voxels_x = 500
    param.n_voxels_y = 500
    param.n_voxels_z = 500
    param.n_pixels_u = 500
    param.n_pixels_v = 500
    param.update_internals()

    domain = barrel_gradient(500)

    #   angles = np.linspace(0., 45., 50)
    #   proj = axis_sym_projection(domain,param,angles=angles)

    #    np.save("proj_barrel_grad",proj)
    proj = np.load("barrel_grad_projections_axisym.npy")

    print("Sigma is ", estimate_sigma(proj))

    proj = np.exp(-proj)

    Reconimg = fdk(proj, param)

    return Reconimg, proj, domain


rec, proj, domain = main()
plt.imshow(rec)
plt.figure()
# plt.show()
plt.plot(rec[200, :], 'g')
plt.plot(rec[:, 250], 'g')
plt.plot(domain[250, :, 250], 'r')
plt.plot(domain[200, 250, :], 'r')

plt.figure()
plt.imshow(np.abs(domain[:250, 250, :] - rec))

plt.show()
