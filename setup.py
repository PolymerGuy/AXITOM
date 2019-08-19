import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="axitom",
    version="0.1.0",
    author="PolymerGuy",
    author_email="sindre.n.olufsen@ntnu.no",
    description="This python package provides tools for axis-symmetric cone-beam computed tomography",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/PolymerGuy/AXITOM",
    packages=setuptools.find_packages(),
    install_requires=[
            'numpy',
            'scipy',
            'pytest',
            'coverage',
            'pytest-cov',
            'codecov',
            'matplotlib',
            'scikit-image',
            'natsort',
            'imageio'
      ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
