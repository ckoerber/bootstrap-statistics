import unittest
from . import core
import bootstats as boot
import os


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
    instances. This includes the parameters, indicies and data members.
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
      bs = type(self.boot)(self.data, **baseKeys)
      self.assertFalse(
        bs == self.boot, 
        msg="Equal test failed for key: {}".format(key)
      )

    # Check for different data
    data = self.data.copy()
    data[0,0] += 1
    bs = type(self.boot)(data, **baseKeys)
    self.assertFalse(
      bs == self.boot, 
      msg="Equal test failed for different data".format(key)
    )

    # Check for different indices
    indices = self.boot.indices.copy()
    indices[0,0] += 1
    bs = type(self.boot)(self.data, indices=indices, NBinSize=self.NBinSize)
    self.assertFalse(
      bs == self.boot, 
      msg="Equal test failed for different data".format(key)
    )


  #-------------------------------
  def test8_exportImport(self):
    """
    Checks wheter output and reading produces the same result. Also checks if 
    exceptions work properly.
    """
    # Export file data
    h5Info = {
      "fileName": "testExport.h5",
      "groupName": "ensemble1"
    }
    # Check wether group already exists in File
    ## External method
    self.assertFalse(
      boot.bootstrapperInHDF5(**h5Info),
      msg="Wrongly identified Bootstrapper export before export"
    )
    ## Class internal method
    self.assertFalse(
      self.boot.inHDF5(**h5Info),
      msg="Wrongly identified Bootstrapper export before export"
    )

    # Export file
    self.boot.exportHDF5(**h5Info)

    # Check wether group now exists in File
    ## External method
    self.assertTrue(
      boot.bootstrapperInHDF5(**h5Info),
      msg="Wrongly did not identify Bootstrapper export after export"
    )
    ## Class internal method
    self.assertTrue(
      self.boot.inHDF5(**h5Info),
      msg="Wrongly did not identify Bootstrapper export after export"
    )

    # Check wether different group exists in File
    ## External method
    self.assertFalse(
      boot.bootstrapperInHDF5(h5Info["fileName"], groupName="notInFile"),
      msg="Wrongly identified not written Bootstrapper export after export"
    )
    ## Class internal method
    self.assertFalse(
      self.boot.inHDF5(h5Info["fileName"], groupName="notInFile"),
      msg="Wrongly identified not written Bootstrapper export after export"
    )

    # Test reading of file
    bs = type(self.boot)(self.data, h5Info=h5Info)
    self.assertEqual(
      bs,
      self.boot, 
      msg="Could not reproduce Bootstrapper after export"
    )

    # Check that overwriting is not possible
    with self.assertRaises(KeyError) as cm:
      bs.exportHDF5(**h5Info)
    # Check if groupName was the issue
    self.assertEqual(
      cm.exception.args[1], h5Info["groupName"],
      msg="Overwriting did not raise expected exception."
    )

    # Test writing sample
    h5Info["groupName"] = "ensemble2"
    bs.exportHDF5(writeSamples=True, **h5Info)
    # Open file
    bootAddress = os.path.join("/", h5Info["groupName"], "bootstrap")
    with boot.h5py.File(h5Info["fileName"], "r") as f:
      bootGroup = f.get(bootAddress)
      ## Read NBinSize
      samples = bootGroup.get("samples").value

    # Compute difference
    diff = core.np.mean(core.np.abs( samples - bs.samples ))/core.np.mean(
      core.np.abs(bs.samples)
    )
    self.assertLess(diff, core.NUMPREC, msg="Exportation of samples failed.")


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
    self.NVars = 128 * 2 * 2
    self.data = core.np.random.normal(
      self.mu, self.var, [128, 2, 2, self.NConfigs]
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
def tearDownModule():
  """Remove temporary files"""
  if os.path.exists('testExport.h5'):
    os.remove('testExport.h5')
#===============================================================================


#===============================================================================
#     Tests
#===============================================================================
if __name__ == "__main__":
  unittest.main()