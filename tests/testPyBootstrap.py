import unittest
from bootstats import PyBootstrap
from . import core


#===============================================================================
class TestDoubleBootstrapper(unittest.TestCase, core.AbstractBootstrapper):
  "Test the 'complex' instantiation of the 'Bootstrapper' wrapper."
  def __init__(self, *args, **kwargs):
    """
    Allocates a random normal data array and constructs a 'DoubleBootstrapper'
    instantiation.
    """
    # Init the parent classes
    super(TestDoubleBootstrapper, self).__init__(*args, **kwargs)
    # Create the data array
    self.data = core.np.random.normal(
      self.mu, self.var, [self.NVars, self.NConfigs]
    )
    # Init the cpp classes
    self.boot = PyBootstrap.DoubleBootstrapper(
      self.data,
      self.NSamples,
      self.NSize,
      self.NBinSize,
    )
#===============================================================================


#===============================================================================
class TestComplexBootstrapper(unittest.TestCase, core.AbstractBootstrapper):
  "Test the 'complex' instantiation of the 'Bootstrapper' wrapper."
  def __init__(self, *args, **kwargs):
    """
    Allocates a random normal data array and constructs a 'DoubleBootstrapper'
    instantiation.
    """
    # Init the parent classes
    super(TestComplexBootstrapper, self).__init__(*args, **kwargs)
    # Create the data array
    tmp = core.np.random.normal(
      self.mu, self.var, [2, self.NVars, self.NConfigs]
    )
    self.data = tmp[0] + 1j* tmp[1]
    # Init the cpp class
    self.boot = PyBootstrap.ComplexBootstrapper(
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