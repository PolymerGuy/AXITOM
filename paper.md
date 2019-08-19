---
title: 'AXITOM: A Python package for reconstruction of axisymmetric tomograms acquired by a conical beam'
tags:
  - Python
  - tomography
  - conical-beam
  - X-ray
authors:
  - name: Sindre Nordmark Olufsen
    affiliation: 1
affiliations:
 - name: Structural Impact Laboratory (SIMLab), Department of Structural Engineering, NTNU, Norwegian University of Science and Technology,
NO-7491 Trondheim, Norway
   index: 1
date: 08 August 2019
bibliography: paper.bib
---

# Summary
The ability to picture the internals of a body in a non-destructive way is vital for both diagnostics and research in a broad range of fields.
Tomography is the imaging of sections within a body and is typically performed by imaging of the body by a penetrating wave and subsequently reconstructing the internals of the body by employing a reconstruction algorithm. There are cases, which allows for simplification of the tomographic problem, 
one of them being the presence of symmetries within the tomogram. Axis-symmetry reduces the tomographic reconstruction into the inversion of the Abel transform, which
can be obtained from a single projection, having a fractional acquisition cost compared to typical datasets. In home-laboratory X-ray setups,
X-rays are distributed in space as a conical beam rather than parallel rays, and such a beam geometry has to be accounted for in the reconstruction of the tomogram.

``AXITOM`` is a Python package which allows for the reconstruction of axis-symmetric tomograms when the projections have been obtained by a conical beam.
Excellent Python packages such as TomoPy [@Gursoy2014] and the Astra toolbox [@Pelt2016; @vanAarle:16; @VANAARLE201535] are already available for tomographic reconstruction,
but are general purpose and does not exploit axis-symmetries. PyAbel [@Hickstein2016] is a Python project for inversion of the Abel transform but is focused on parallel beam geometries.

``AXITOM`` contains a collection of high-level functions which can be used to load datasets, perform virtual experiments and perform the tomographic reconstruction.
A Feldkamp David Kress algorithm [@Feldkamp:84] is used to reconstruct the tomograms, and the modifications made to the algorithm are
for reduced computational cost. The implementation relies on the use of the Numpy[@Numpy] and  Scipy[@Scipy], as well as numerous packages for visualization and IO.

``AXITOM`` was implemented for the reconstruction axis-symmetric density fields measured by X-ray absorption radiography.
This project is a part of the ongoing research within the SFI CASA research group at NTNU and has been a key component in the pursuit of *in-situ* 
investigation of cavitation of polymers during deformation.

# Acknowledgements
The author gratefully appreciates the financial support from the Research Council of Norway through the Centre for Advanced Structural Analysis, Project No. 237885 (SFI-CASA).
# References
