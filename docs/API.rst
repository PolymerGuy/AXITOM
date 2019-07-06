.. AXITOM documentation master file, created by
   sphinx-quickstart on Tue Jun 25 21:12:55 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

API documentation
=================


Back projection
--------------

.. autofunction:: FDK.backprojection.map_object_to_detector_coords


.. autofunction:: FDK.backprojection.fdk


Forward projection
--------------

.. autofunction:: FDK.projection.forward_project


.. autofunction:: FDK.projection.axis_sym_projection



Filtering
---------

.. autofunction:: FDK.filtering.ramp_kernel_real


.. autofunction:: FDK.filtering.add_weights


.. autofunction:: FDK.filtering.ramp_filter_and_weight


Parse files
-----------

.. autofunction:: FDK.phantoms.parse_xtekct_file


Phantoms
--------

.. autofunction:: FDK.phantoms.barrel

.. autofunction:: FDK.phantoms.barrel_gradient


Utilities
---------

.. autofunction:: FDK.utilities.find_center_of_gravity_in_radiogram

.. autofunction:: FDK.phantoms.object_center_of_rotation

.. autofunction:: FDK.phantoms.rotate_coordinates

.. autofunction:: FDK.phantoms.list_files_in_folder

.. autofunction:: FDK.phantoms.shading_correction

.. autofunction:: FDK.phantoms.read_image
