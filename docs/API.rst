

API documentation
=================
This document contains the documentation contained within the docstrings of all available functions and classes.


Back projection
---------------

.. autofunction:: axitom.backprojection.map_object_to_detector_coords


.. autofunction:: axitom.backprojection.fdk


Forward projection
------------------

.. autofunction:: axitom.projection.axis_sym_projection


Config
------

.. autofunction:: axitom.config.config_from_xtekct

.. autoclass:: axitom.config.Config
   :members:

   .. automethod:: __init__


Filtering
---------

.. autofunction:: axitom.filtering.ramp_kernel_real


.. autofunction:: axitom.filtering.add_weights


.. autofunction:: axitom.filtering.ramp_filter_and_weight


Parse files
-----------

.. autofunction:: axitom.parse.parse_xtekct_file


Phantoms
--------

.. autofunction:: axitom.phantoms.barrel


Utilities
---------

.. autofunction:: axitom.utilities.find_center_of_gravity_in_radiogram

.. autofunction:: axitom.utilities.object_center_of_rotation

.. autofunction:: axitom.utilities.rotate_coordinates

.. autofunction:: axitom.utilities.list_files_in_folder

.. autofunction:: axitom.utilities.shading_correction

.. autofunction:: axitom.utilities.read_image
