#!/usr/bin/env python
from setuptools import setup, find_packages
from distutils.extension import Extension
from Cython.Distutils import build_ext
import os


# Requirements
installRequires = ["numpy", "cython", "h5py"]

#-------Building the C++ extension---------
sources          = [
  os.path.join("bootstats", "PyBootstrap.pyx"), 
  os.path.join("bootstats", "cFiles", "Bootstrap.cpp"),
]
language         = "c++"
extraCompileArgs = ["-std=c++14", "-pedantic", "-Wno-c++1z-extensions"]

ext_modules=[
  Extension(
    os.path.join("bootstats", "PyBootstrap"),
    sources            = sources,
    language           = language,
    extra_compile_args = extraCompileArgs,
  ),
]

#-------Building the module---------
# Setup module
long_description = """Python wrapper for C++ routine which computes bootstrap 
distributions of the mean for randomly distributed variables."""

setup(
  name             = "bootstrap-statistics",
  version          = "0.1",
  description      = "Python API for Bootstrapping data",
  long_description = long_description,
  author           = "Christopher Koerber",
  author_email     = "c.koerber@fz-juelich.de",
  cmdclass         = {"build_ext": build_ext},
  ext_modules      = ext_modules,
  license          = 'MIT',
  install_requires = installRequires,
  packages         = ['bootstats'],
  keywords         = "Bootstrap Statistics",
  test_suite       = 'tests',
  url              = "https://github.com/ckoerber/bootstrap-statistics"
)