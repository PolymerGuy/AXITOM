.. AXITOM documentation master file, created by
   sphinx-quickstart on Tue Jun 25 21:12:55 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

FDK
===
The Feldkamp David Kress (FDK) algorithm is often used in the reconstruction of tomographic data where the radiograms are
acquired using a conical X-ray beam. The original article is found here:

    Feldkamp, L. A. (1984). Practical cone-beam algorithm Sfrdr I _ f. America, 1(6), 612–619. https://doi.org/10.1364/JOSAA.1.000612

The notation we will use in the following document is taken from this thesis:

    Turbell, H. (2001). Cone-Beam Reconstruction Using Filtered Backprojectionn. Science And Technology. Retrieved from http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.134.5224&amp;rep=rep1&amp;type=pdf

Full 3D reconstruction is usually performed using this algorithm, but we will here modify is slightly to
more efficiently reconstruct an axisymmetric tomogram.


Full 3D reconstruct
-------------------

In its original form, the reconstructed tomogram :math:`f_{FDK}(x,y,z)` is determined by the following equation:



.. math::
   :nowrap:


    \begin{equation}
    f_{FDK}(x,y,z) = \int_0^{2\pi} \frac{R^2}{U(x,y,\beta)^2} \tilde{p}^F (\beta, a(x,y,\beta),b(x,y,z,\beta))d\beta
    \end{equation}

where 

.. math::
   :nowrap:

    \begin{equation}
    \tilde{p}^F(\beta,a,b) = (\frac{R}{\sqrt[]{R^2+a^2+b^2}} p (\beta,a,b)) * g^P(a)
    \end{equation}

is the filtered and weighted radiograms. :math:`p (\beta,a,b)` is the radiogram acquired for 
angle :math:`\beta` wheras :math:`a` and :math:`b` denotes the sensor coordinates and :math:`R` is the sensor to specimen distance.
A ramp filter :math:`g^P(a)` is applied in the horizontal direction of the sensor by means of convolution.


The term :math:`U(x,y,\beta)` is determined by:

.. math::
   :nowrap:

    \begin{equation}
    U(x,y,\beta) = R +x\cos \beta + y \sin \beta
    \end{equation}

where :math:`x` and :math:`y` are coordinates to material points in the specimen.

The sensor coordinates :math:`a` and :math:`b` corresponding to the material point defined by the :math:`x`, :math:`y` and :math:`z` coordinates,
for a given angle :math:`\beta` can be determined by:


.. math::
   :nowrap:

    \begin{equation}
    a(x,y,\beta) = R \frac{-x \sin \beta + y \cos \beta}{R + x \cos \beta + y \sin \beta}
    \end{equation}

.. math::
   :nowrap:

    \begin{equation}
    b(x,y,z\beta) = z \frac{R}{R+x\cos \beta + y \sin \beta}
    \end{equation}


Axis-symmetry
-------------
In the case where the tomogram :math:`f_{FDK}(x,y,z)` is axisymmetric around a rotational axis tomogram :math:`z`, all radial 
slices of the tomogram should be equal.

We here reduce the tomographic problem by assuming that all projections :math:`p` are independent of :math:`\beta`,
and we reconstruct only the plaing laying in :math:`x=0` giving:


.. math::
   :nowrap:

    \begin{equation}
    f_{FDK}(y,z) = \int_0^{2\pi} \frac{R^2}{U(y,\beta)^2} \tilde{p}^F ( a(y,\beta),b(y,z,\beta))d\beta
    \end{equation}

where 

.. math::
   :nowrap:

    \begin{equation}
    a(y,\beta) = R \frac{ y \cos \beta}{R + y \sin \beta}
    \end{equation}

.. math::
   :nowrap:

    \begin{equation}
    b(y,z\beta) = z \frac{R}{R+ y \sin \beta}
    \end{equation}
    
The values of :math:`\tilde{p}^F (a(x,y,\beta),b(x,y,z,\beta))` are obtained by means of interpolation employing bi-cubic splines.



