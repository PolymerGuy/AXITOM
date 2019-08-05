

<!-- PROJECT SHIELDS -->

[![CircleCI](https://circleci.com/gh/PolymerGuy/AXITOM.svg?style=svg)](https://circleci.com/gh/PolymerGuy/AXITOM)
[![codecov](https://codecov.io/gh/PolymerGuy/AXITOM/branch/master/graph/badge.svg)](https://codecov.io/gh/PolymerGuy/AXITOM)
[![MIT License][license-shield]][license-url]
[![Documentation Status](https://readthedocs.org/projects/axitom/badge/?version=latest)](https://axitom.readthedocs.io/en/latest/?badge=latest)


<!-- PROJECT LOGO -->
<br />
<p align="center">
  <a href="https://github.com/othneildrew/Best-README-Template">
    <img src="./docs/logo.png" alt="Logo" width="500" height="500">
  </a>

  <h3 align="center">AXITOM</h3>

  <p align="center">
    Tomographic reconstruction of axisymmetric fields acquired by a cone beam geometry
    <br />
    <a href="https://axitom.readthedocs.io/en/latest/"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/othneildrew/Best-README-Template">View Demo</a>
    ·
    <a href="https://github.com/othneildrew/Best-README-Template/issues">Report Bug</a>
    ·
    <a href="https://github.com/othneildrew/Best-README-Template/issues">Request Feature</a>
  </p>
</p>





<!-- ABOUT THE PROJECT -->
About The Project
-----------------
This python package provides tools for axis-symmetric cone beam computed tomography. The reconstruction is performed by a Feldkamp David Kress algorihtm
which have been adapted such that is exploits the axis-symmetric nature of the the tomogram.

This toolkit has a highly spezialised usage, and there are plenty of more general and excellent frameworks for tomographic reconstruction, such as:
 * [TomoPy](https://github.com/tomopy/tomopy) (General computed tomography, cone and parallel beam geometry)
 * [PyAbel](https://github.com/PyAbel/PyAbel) (Computed tomography based on the inverse Abel transform, parallel beam geometry)
 
 This project aims at providing a simple an accessible tool-kit for forward projection and reconstruction of 
 axis-symmetric tomograms based on a conical beam geometry.

### Built With
This project is heavily based on the following packages:
* [Numpy](https://numpy.org/)
* [Scipy](https://www.scipy.org/)
* [Scikit-image](https://scikit-image.org/)
* [Matplotlib](https://matplotlib.org/)



<!-- GETTING STARTED -->
Getting Started
---------------

This is an example of how you may give instructions on setting up your project locally.
To get a local copy up and running follow these simple example steps.

### Clone the repo:

These instructions will get you a copy of the project up and running on your 
local machine for development and testing purposes.

Prerequisites:
    This toolkit is tested on Python 3.7

Installing:
Start to clone this repo to your preferred location

    $ git init
    $ git clone https://github.com/PolymerGuy/axitom.git
    
We recommend that you always use virtual environments, either by virtualenv or by Conda env
    
    $ python -m virtualenv env
    $ source ./env/bin/activate #On Linux and Mac OS
    $ env\Scripts\activate.bat #On Windows
    $ pip install -r requirements.txt

You can now run an example::
    
    $ python <path_to_axitom>/Examples/quick_start.py

### Run the tests
The tests should always be launched to check your installation.
These tests are integration and unit tests

If you installed via a package manger

    $ nosetests axitom

If you cloned the repo, you have to call nosetests from within the folder

    $ nosetests axitom


Example
-------
Let's now go through the necessary steps for doing reconstruction of a tomogram based on a single image.
First, we need to import the tools

    import axitom as tom
    from scipy.ndimage.filters import median_filter

Assuming that the example data from the repo is located in the example_data folder, we can make a config object
from the .xtekct file

    config = tom.config_from_xtekct("./example_data/R02_01.xtekct")

We now import the radiogram

     radiogram = tom.read_image(r"./example_data/R02_01.tif, flat_corrected=True)

And we remove the top and bottom of the image. This is necessary in this example, as the fixtures will interfere with
the algorithm used to find the center of rotation

     radiogram[:250, :] = 0.95
     radiogram[1800:, :] = 0.95

As we will use a single radiogram only in this reconstruction, we will reduce the noise content of the radiogram by
employing a median filter. This works fine since the density gradients within the specimen are relatively small.
You may here choose any filter of your liking

     radiogram = median_filter(radiogram, size=20)

Now, the axis of rotation has to be determined. This is done be binarization of the image into object and background
and determining the center of gravity of the object

     _, center_offset = tom.object_center_of_rotation(radiogram, config, background_internsity=0.9)

The config object has to be updated with the correct values

     config.center_of_rot_y = center_offset
     config.update_internals()

We are now ready to initiate the reconstruction

     tomo = tom.fdk(radiogram, config)


The results can then be visualized

   plt.title("Radial slice")
   plt.imshow(tomo.transpose(), cmap=plt.cm.magma)
   

<img src="./docs/results.png" alt="Results" width="300"/>

<!-- CONTRIBUTING -->
Contributing
------------

Contributions are what make the open source community such an amazing place to be learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request


<!-- LICENSE -->
License
-------

Distributed under the MIT License. See `LICENSE` for more information.

<!-- CONTACT -->
Contact
-------

Sindre Nordmark Olufsen (PolymerGuy) - sindre.n.olufsen@ntnu.no


<!-- ACKNOWLEDGEMENTS -->
Acknowledgements
----------------
We are in great debt to the open source community and all the contributors the the projects on which this toolkit is based.

<!-- MARKDOWN LINKS & IMAGES -->
[license-shield]: https://img.shields.io/badge/license-MIT-blue.svg?style=flat-square
[license-url]: https://choosealicense.com/licenses/mit

