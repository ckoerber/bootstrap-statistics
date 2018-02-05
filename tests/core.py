import numpy as np

NUMPREC = 1.e-12

#===============================================================================
#     Tests
#===============================================================================
class AbstractBootstrapper(object):
  """
    Abstract class which executes the meta tests for each 'Bootstrapper' 
    instantiation.
  """
  # Static members
  #-------------------------------
  NVars    = 128
  NConfigs = 1001

  NSamples = 400
  NBinSize = 5
  NBins    = int(NConfigs/NBinSize)
  NSize    = NBins

  mu       = 0.0
  var      = 1.0

  data     = None
  boot     = None
  #-------------------------------
  def test1_ConstructorParameter(self):
    """
    Test the construction of the 'Bootstrapper' instantiation.
      -> compares the sizes of internal arrays and members
    """
    # Check members
    self.assertEqual(self.NVars,    self.boot.NVars   )
    self.assertEqual(self.NConfigs, self.boot.NConfigs)
    self.assertEqual(self.NSamples, self.boot.NSamples)
    self.assertEqual(self.NBinSize, self.boot.NBinSize)
    self.assertEqual(self.NSize,    self.boot.NSize   )
    self.assertEqual(self.NBins,    self.boot.NBins   )

    # Check data shape
    self.assertEqual((self.NVars, self.NBins), self.boot.data.shape)

    # Check random indices shape
    self.assertEqual((self.NSamples, self.NSize), self.boot.indices.shape)

  #-------------------------------
  def test2_ConstructorIndices(self):
    """
    Test the construction of the 'Bootstrapper' instantiation.
    Now construcs bootstrapper from indices.
      -> compares the sizes of internal arrays and members
    """
    # Instantiate new Bootstrapper by using available indices
    boot = type(self.boot)(
      self.data, 
      NBinSize=self.NBinSize, 
      indices=self.boot.indices
    )
    
    # Check members
    self.assertEqual(boot.NVars,    self.boot.NVars   )
    self.assertEqual(boot.NConfigs, self.boot.NConfigs)
    self.assertEqual(boot.NSamples, self.boot.NSamples)
    self.assertEqual(boot.NBinSize, self.boot.NBinSize)
    self.assertEqual(boot.NSize,    self.boot.NSize   )
    self.assertEqual(boot.NBins,    self.boot.NBins   )

    # Check data shape
    self.assertEqual((self.NVars, self.NBins), boot.data.shape)

    # Check data equality
    ## to aggregate data and compute the mean of the absolute difference
    dataDiff = np.average(np.abs(boot.data - self.boot.data))
    self.assertLess(
      dataDiff,
      NUMPREC,
      msg="Parameter constructor data different from indicies constructor data."
    )

    # Check random indices shape
    self.assertEqual((self.NSamples, self.NSize), boot.indices.shape)

    # Check indices equality
    ## to aggregate data and compute the mean of the absolute difference
    indicesDiff = np.average(np.abs(boot.indices - self.boot.indices))
    self.assertLess(
      indicesDiff,
      NUMPREC,
      msg="Parameter constructor indices different from indicies constructor data."
    )

  #-------------------------------
  def test3_Binning(self):
    """
    Test the construction of the 'Bootstrapper' instantiation.
      -> compares the binnign of the input data binning
    """
    # Check if data equal
    ## Do numpy binning -> drop initial modulo bins and reshape
    binned = self.data[:, self.NConfigs%self.NBinSize: ].reshape(
      [self.NVars, self.NBins, self.NBinSize]
    )

    ## to aggregate data and compute the mean of the absolute difference
    dataDiff = np.average(np.abs(np.average(binned, axis=2) - self.boot.data))
    self.assertLess(
      dataDiff,
      NUMPREC,
      msg="C++ binned data unequal numpy binned data."
    )

  #-------------------------------
  def test4_UniformDistribution(self):
    """
    Tests wether the random number generator actually computes a uniform 
    distribution.
    """
    # check if all numbers in the right range are present
    self.assertEqual(
      list(range(self.NBins)), 
      list(np.unique(self.boot.indices)),
      msg="Random number generator does not reproduce the full spectrum." +
          " You might have to increase 'NSamples' or 'NSize' to do so..."
    )
    # Now check distribution
    ## This is done by binning the data and computing the standard deviation
    ## of the mean. If this number is too large, it is considered non-uniform
    vals, bins = np.histogram(self.boot.indices, bins=10)
    deviation  = np.std(vals) / np.mean(vals)
    self.assertLess(
      deviation, 
      2./100, 
      msg="Standard deviation from perfect uniform spectrum is more than 2%"
    )

  #-------------------------------
  def test5_BinnedDataMean(self):
    """
    Tests wether the mean of the binned data is computed correctly.
    """
    meanDiff = np.average(np.abs(
      np.average(self.boot.data, axis=1)-self.boot.mean
    ))
    self.assertLess(meanDiff, NUMPREC)

  #-------------------------------
  def test6_Sampling(self):
    """
    Test wether the sampling works correctly for given indices and bins.
    """
    # Check shape of samples
    cppSamples = self.boot._getSamples()
    self.assertEqual( (self.NVars, self.NSamples), cppSamples.shape )
    # Check values of samples
    numpySamples = np.average(self.boot.data[:,self.boot.indices], axis=2)
    samplesDiff = np.average(np.abs( numpySamples - cppSamples ))
    self.assertLess(samplesDiff, NUMPREC)


#===============================================================================