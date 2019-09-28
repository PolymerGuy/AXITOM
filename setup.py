import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="axitom",
    version="0.1.3",
    author="PolymerGuy",
    author_email="sindre.n.olufsen@ntnu.no",
    description="Tools for axis-symmetric cone-beam computed tomography",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/PolymerGuy/AXITOM",
    include_package_data=True,
    packages=setuptools.find_packages(),
    install_requires=[
            'numpy',
            'scipy',
            'matplotlib',
            'scikit-image',
            'natsort',
            'imageio',
            'nose'
      ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
