Installation
=============
In order to get started with AXITOM, you need to install it on your computer.
There are two main ways to to this:

*   You can install it via a package manager like PIP or Conda
*   You can  clone the repo

By cloning the repo:
---------------------

These instructions will get you a copy of the project up and running on your 
local machine for development and testing purposes.

Prerequisites:
    This toolkit is tested on Python 3.7

Start to clone this repo to your preferred location::

   git init
   git clone https://github.com/PolymerGuy/axitom.git



We recommend that you always use virtual environments, either by virtualenv or by Conda env

Virtual env::

    python -m virtualenv env
    source ./env/bin/activate #On Linux and Mac OS
    env\Scripts\activate.bat #On Windows
    pip install -r requirements.txt


You can now run an example::

    $ python path_to_axitom/Examples/quick_start.py



Running the tests
------------------
The tests should always be launched to check your installation.
These tests are integration and unit tests

If you installed via a package manger::

    nosetests axitom

If you cloned the repo, you have to call nosetests from within the folder::

    nosetests axitom

