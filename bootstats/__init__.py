#!/usr/bin/env python
import PyBootstrap
import numpy as np
import h5py
import os


NUMPREC = 1.e-14

#-------------------------------------------------------------------------------
class Bootstrapper(object):
  """Bootstrapper class for mean distribution estimation."""
  #------------------
  def __init__(
    self, 
    data, 
    NSamples=None, 
    NSize=None, 
    NBinSize=None, 
    indices=None
  ):
    """
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
      "NBins":    self.NBins,
    }

    ## Dictionary containing informative parameters
    self._samples = None

  #------------------
  def _getSamples(self):
    """!
    Compute the bootstrap samples of size 'self.NVars x self.NSamples'.
    This routines uses 'self.indices' to reshape 'self.data' before averaging.
    The averaged out dimension is 'self.NSize'.

    This is the most expensive computation. The output array is not stored
    within this class. Make sure, if you want to use it, to store it elsewhere.
    """
    return self.boot._getSamples()

  #------------------
  @property
  def samples(self):
    """
    The bootstrap samples of size 'self.NVars x self.NSamples'.
    This routines uses 'self.indices' to reshape 'self.data' before averaging.
    The averaged out dimension is 'self.NSize'.

    This is the most expensive computation. For this reason this array
    is initialized only after accesing this member and stored afterwards.
    """
    if self._samples is None:
      self._samples = self._getSamples()
    return self._samples

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

  #------------------
  def __eq__(self, other):
    """
    Compares wheter the other has the same input parameter and data.
    """
    # Check whether other is Bootstrapper
    if not(isinstance(other, Bootstrapper)):
      return False
    else:
      # Iterate through parameters
      for key, val in self.parameters.items():
        if other.parameters[key] != val:
          return False
      # Compare indices
      if not( (self.indices == other.indices).all() ):
        return False
      # Check data
      diff = 2*np.mean( np.abs(self.data - other.data) )
      mean = max(2, np.mean( np.abs(self.data + other.data) ) )
      if diff / mean > NUMPREC * self.NSize:
        return False

      # All checks passed
      return True

  #------------------
  def exportHDF5(self, fileName, groupName=None, writeSamples=False):
    """
    
    """
    # Check if already in hdf5 file first
    if os.path.exists(fileName):
      mode = "a"
    else:
      mode = "w"

    # Specify the root address for writing
    ROOT = "/"
    if groupName is None:
      baseAddress = ROOT
    else:
      baseAddress = os.path.join(ROOT, groupName)

    # And the data is stored in
    bootAddress = os.path.join(baseAddress, "bootstrap")

    # Open the HDF5 file
    with h5py.File(fileName, mode) as f:
      # Check whether group already exists
      baseGroup = f.get(baseAddress)
      if baseGroup is None:
        baseGroup = f.create_group(baseAddress)
      # Check wether bootstrap data exists
      if "bootstrap" in baseGroup.keys():
        raise KeyError("Group 'bootstrap' already exist for base " + \
          "group {}. Stop writing".format(groupName)
        )
      bootGroup = f.create_group(bootAddress)

      # Now write parameters
      for key, val in self.parameters.items():
        bootGroup.create_dataset(key, data=val)
      # Write indices
      bootGroup.create_dataset("indices", data=self.indices)
      # Write samples if requested
      if writeSamples:
        bootGroup.create_dataset("samples", data=self.samples)