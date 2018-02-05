#!/usr/bin/env python
import PyBootstrap
import numpy as np


#-------------------------------------------------------------------------------
class Bootstrapper(object):
  """Bootstrapper class for ensemble data set. Wraps the classes in PyBootstrap"""
  #------------------
  def __init__(
    self, 
    data, 
    NSamples=None, 
    NSize=None, 
    NBinSize=None, 
    indices=None
  ):
    """!
    Initialize the 'Bootstrapper'.
    This must be done by either specifying 
      - [data, NSamples, NSize, NBinSize], or
      - [data, indices, NBinSize]

    @param data     numpy array of size NVars x NConfigs 
    @param NSamples the number of to be drawn bootstrap samples
    @param NSize    the size of each bootstrap sample
    @param NBinSize the size if in which the data is binned 
    @param indices  given set of indices (size #NSamples x #NSize)
    """
    # initialize the C++ object
    # Check data type
    if isinstance(data[0,0], float):
      self.boot = PyBootstrap.DoubleBootstrapper(
        data, 
        NSamples=NSamples, 
        NSize=NSize, 
        NBinSize=NBinSize, 
        indices=indices
      )
    elif isinstance(data[0,0], complex):
      self.boot = PyBootstrap.ComplexBootstrapper(
        data, 
        NSamples=NSamples, 
        NSize=NSize, 
        NBinSize=NBinSize, 
        indices=indices
      )
    else:
      raise TypeError("Input data needs to be of type 'float' or 'complex'")

    # set the members
    ## The number of to be generated bootstrap samples.
    self.NSamples = self.boot.NSamples
    ## The number of bins contained in each individual bootstrap sample.
    self.NSize    = self.boot.NSize
    ## The number of configurations contained in one bin.
    self.NBinSize = self.boot.NBinSize
    ## The number of configurations in the ensemble. This is the first dimension of the input array.
    self.NConfigs = self.boot.NConfigs
    ## The number of variables in the ensemble. Second dimension of the input array.
    self.NVars    = self.boot.NVars
    ## The number of bins given by #NConfigs/#NBinSize.
    ## In case mod(#NConfigs, #NBinSize) != 0, the remainder is skipped at the 
    #  beginning of the input data array.
    self.NBins    = self.boot.NBins
    ## The binned data of size #NVars x #NBins.
    # Note that this is not the input data.
    self.data     = self.boot.data
    ## The bootstrap indicies of size #NSamples x #NSize.
    self.indices  = self.boot.indices
    ## Returns the mean of the #data.
    # \note This mean is also equal to the mean of the input data modulo the 
    # binning cutoff.
    self.mean     = self.boot.mean

    ## Dictionary containing informative parameters
    self.parameters = {
      "NSamples": self.NSamples,
      "NSize":    self.NSize,
      "NBinSize": self.NBinSize,
      "NConfigs": self.NConfigs,
      "NVars":    self.NVars,
    }

  #------------------
  def getSamples(self):
    """!
    Compute the bootstrap samples of size #NVars x #NSamples.
    This routines uses #indices to reshape #data.
    The averaged out dimension is #NSize.

    This is the most expensive computation. The output array is not stored
    within this class. Make sure, if you want to use it, to store it elsewhere.
    """
    return self.boot.getSamples()

  #------------------
  def getCov(self, samples=None):
    """!
    Computes the covariance matrix form the bootstrap samples.

    @param samples (optional) Bootstrap samples computed by #getSamples()

    This function also calls #getSamples() in case you do not specify the
    covariance matrix. Thus, in case you are interested in the samples as well,
    better call #getSamples() and feed it to this method.
    """
    return self.boot.getCov(samples=samples)

  #------------------
  def __str__(self):
    """Returns name and input parameters"""
    return "Bootstrapper(" + ", ".join([
      "{key}={val}".format(key=key, val=val) 
        for key, val in self.parameters.items()
    ]) + ")"

  #------------------
  def __repr__(self):
    return str(self)