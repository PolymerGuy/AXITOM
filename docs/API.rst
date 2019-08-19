

API documentation
=================
This document contains the documentation contained within the docstrings of all available functions and classes.


Back projection
---------------

.. autofunction:: FDK.backprojection.map_object_to_detector_coords


.. autofunction:: FDK.backprojection.fdk


Forward projection
------------------

.. autofunction:: FDK.projection.axis_sym_projection


Config
------

.. autofunction:: FDK.config.config_from_xtekct

.. autoclass:: FDK.config.Config
   :members:

   .. automethod:: __init__


Filtering
---------

.. autofunction:: FDK.filtering.ramp_kernel_real


.. autofunction:: FDK.filtering.add_weights


.. autofunction:: FDK.filtering.ramp_filter_and_weight


Parse files
-----------

.. autofunction:: FDK.parse.parse_xtekct_file


Phantoms
--------

.. autofunction:: FDK.phantoms.barrel


Utilities
---------

.. autofunction:: FDK.utilities.find_center_of_gravity_in_radiogram

.. autofunction:: FDK.utilities.object_center_of_rotation

.. autofunction:: FDK.utilities.rotate_coordinates

.. autofunction:: FDK.utilities.list_files_in_folder

.. autofunction:: FDK.utilities.shading_correction

.. autofunction:: FDK.utilities.read_image
