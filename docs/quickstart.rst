.. AXITOM documentation master file, created by
   sphinx-quickstart on Tue Jun 25 21:12:55 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Quick start
==========

Let's now go through the necessary steps for doing reconstruction of a tomogram based on a single image.
First, we need to import the tools::

    import axitom as tom
    from scipy.ndimage.filters import median_filter

Assuming that the example data from the repo is located in the example_data folder, we can make a config object
from the .xtekct file::

    config = tom.config_from_xtekct("./example_data/R02_01.xtekct")

We now import the radiogram::

     radiogram = tom.read_image(r"./example_data/R02_01.tif", flat_corrected=True)

And we remove the top and bottom of the image. This is necessary in this example, as the fixtures will interfere with
the algorithm used to find the center of rotation::

     radiogram[:250, :] = 0.95
     radiogram[1800:, :] = 0.95

As we will use a single radiogram only in this reconstruction, we will reduce the noise content of the radiogram by
employing a median filter. This works fine since the density gradients within the specimen are relatively small.
You may here choose any filter of your liking::

     radiogram = median_filter(radiogram, size=20)

Now, the axis of rotation has to be determined. This is done be binarization of the image into object and background
and determining the center of gravity of the object::

     _, center_offset = tom.object_center_of_rotation(radiogram, config, background_internsity=0.9)

The config object has to be updated with the correct values::

     config.center_of_rot_y = center_offset
     config.update()

We are now ready to initiate the reconstruction::

     tomo = tom.fdk(radiogram, config)


The results can then be visualized::

   import matplotlib.pyplot as plt
   plt.title("Radial slice")
   plt.imshow(tomo.transpose(), cmap=plt.cm.magma)

and looks like this:

.. image:: results.png
   :scale: 30 %
   :alt: The results
   :align: center