import unittest
from . import core
import bootstats as boot


#===============================================================================
#     Extension of core abstract test
#===============================================================================
class AbstractBootstrapper(core.AbstractBootstrapper):
  """
  Extends 'core.AbstractBootstrapper' by methods specific to 'boot.Bootstrapper'
  """

  #-------------------------------
  def test7_equalness(self):
    """
    Checks wheter the equal method correcly identifies equal 'Bootstrapper'
    instances.
    """
    # Check self
    self.assertTrue(self.boot == self.boot)

    # Setup basic initialization
    baseKeys = {}
    for key in ["NSamples", "NSize", "NBinSize"]:
      baseKeys[key] = self.boot.parameters[key]

    # Check for different parameters
    ## Change each parameter for initialization
    for key in ["NSamples", "NSize", "NBinSize"]:
      pars = baseKeys.copy()
      pars[key] +=1
      boot = type(self.boot)(self.data, **baseKeys)
      self.assertFalse(
        boot == self.boot, 
        msg="Equal test failed for key: {}".format(key)
      )

    # Check for different data
    data = self.data.copy()
    data[0,0] += 1
    boot = type(self.boot)(data, **baseKeys)
    self.assertFalse(
      boot == self.boot, 
      msg="Equal test failed for different data".format(key)
    )

    # Check for different indices
    indices = self.boot.indices.copy()
    indices[0,0] += 1
    boot = type(self.boot)(self.data, indices=indices, NBinSize=self.NBinSize)
    self.assertFalse(
      boot == self.boot, 
      msg="Equal test failed for different data".format(key)
    )


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
    self.data = core.np.random.normal(
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
class TestBootstrapperComplex(unittest.TestCase, core.AbstractBootstrapper):
  "Test the 'complex' instantiation of the 'Bootstrapper' wrapper."
  def __init__(self, *args, **kwargs):
    """
    Allocates a random normal data array and constructs a 'Bootstrapper' with
    complex data.
    """
    # Init the parent classes
    super(TestBootstrapperComplex, self).__init__(*args, **kwargs)
    # Create the data array
    tmp = core.np.random.normal(
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