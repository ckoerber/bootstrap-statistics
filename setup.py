#!/usr/bin/env python
from setuptools import setup, find_packages
from distutils.extension import Extension
from Cython.Distutils import build_ext


# Make readme available
def readme():
  with open("README.md") as f:
    return f.read()

# Requirements
installRequires = ["numpy", "cython"]

#-------Building the C++ extension---------
sources          = ["bootstats/PyBootstrap.pyx", "bootstats/Bootstrap.cpp",]
language         = "c++"
extraCompileArgs = ["-std=c++17", "-pedantic",]

ext_modules=[
  Extension(
    "PyBootstrap",
    sources            = sources,
    language           = language,
    extra_compile_args = extraCompileArgs,
  ),
]

#-------Building the module---------
# Setup module
setup(
  name             = "bootstrap-statistics",
  version          = "0.1",
  description      = "Python API for Bootstrapping data",
  long_description = readme(),
  author           = "Christopher Koerber",
  author_email     = "c.koerber@fz-juelich.de",
  cmdclass         = {"build_ext": build_ext},
  ext_modules      = ext_modules,
  license          = 'MIT',
  install_requires = installRequires,
  packages         = ['bootstats'],
  keywords         = "Bootstrap Statistics",
  test_suite       = 'tests'
)