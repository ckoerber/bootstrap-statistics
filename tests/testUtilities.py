#!/usr/bin/env python
import unittest
import numpy as np
from .testPyBootstrap import AbstractBootstrapper, NUMPREC
import bootstats as boot

NUMPREC = 1.e-7

#===============================================================================
#     Tests
#===============================================================================


#===============================================================================
class TestBootstrapperDouble(unittest.TestCase, AbstractBootstrapper):
  "Test the 'double' instantiation of the 'Bootstrapper' wrapper."
  def __init__(self, *args, **kwargs):
    """
    Allocates a random normal data array and constructs a 'Bootstrapper' with
    double data.
    """
    # Init the parent classes
    super(TestBootstrapperDouble, self).__init__(*args, **kwargs)
    # Create the data array
    self.data = np.random.normal(
      self.mu, self.var, [self.NVars, self.NConfigs]
    )
    # Init the cpp class
    self.boot = boot.Bootstrapper(
      self.data,
      self.NSamples,
      self.NSize,
      self.NBinSize,
    )
#===============================================================================



#===============================================================================
class TestBootstrapperComplex(unittest.TestCase, AbstractBootstrapper):
  "Test the 'complex' instantiation of the 'Bootstrapper' wrapper."
  def __init__(self, *args, **kwargs):
    """
    Allocates a random normal data array and constructs a 'Bootstrapper' with
    complex data.
    """
    # Init the parent classes
    super(TestBootstrapperComplex, self).__init__(*args, **kwargs)
    # Create the data array
    tmp = np.random.normal(
      self.mu, self.var, [2, self.NVars, self.NConfigs]
    )
    self.data = tmp[0] + 1j* tmp[1]
    # Init the cpp class
    self.boot = boot.Bootstrapper(
      self.data,
      self.NSamples,
      self.NSize,
      self.NBinSize,
    )
#===============================================================================



#===============================================================================
#     Tests
#===============================================================================
if __name__ == "__main__":
  unittest.main()