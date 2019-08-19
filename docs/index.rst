.. AXITOM documentation master file, created by
   sphinx-quickstart on Tue Jun 25 21:12:55 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to AXITOM's documentation!
==================================

This python package provides tools for axis-symmetric cone-beam computed tomography. A Feldkamp David Kress algorithm performs the reconstruction
which have been adapted such that is exploits the axis-symmetric nature of the tomogram.

This toolkit has a highly specialised usage, and there are plenty of more general and excellent frameworks for tomographic reconstruction, such as:

 * TomoPy (https://github.com/tomopy/tomopy) General computed tomography, cone and parallel beam geometry
 * PyAbel (https://github.com/PyAbel/PyAbel) Computed tomography based on the inverse Abel transform, parallel beam geometry

This project aims at providing a simple, accessible toolkit for forward-projection and reconstruction of
axis-symmetric tomograms based on a conical beam geometry.


.. toctree::
   :maxdepth: 2
   :caption: Getting started:

   install
   quickstart


.. toctree::
   :maxdepth: 2
   :caption: API:

   API

.. toctree::
   :maxdepth: 2
   :caption: Theory:

   FDK

.. toctree::
   :maxdepth: 2
   :caption: Verification:

   Comparison