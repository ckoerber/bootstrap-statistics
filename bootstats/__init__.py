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
    indices=None,
    h5Info=None,
  ):
    """
    Bootstrapper class which can be used to compute the bootstrapped 
    distribution of the means of input data 'data'. If 'NBinSize' is larger than
    one, the input data will be binned before it is sampled.

    The class can be initialized in three different ways:
        1. Parameter initialization with [NSamples, NSize, NBinsize] specified,
        2. Indices initialization with [indices, NBinSize] specified,
        3. File initialization with h5Info specified.
    Independent on the initialization choice, one must specify the input data.

    Parameters
    ----------
    data : two-dimensional ndarray (NVars x NConfigs), float or complex
        Input data which is used to compute the bootstrapped distribution of 
        the means. The first dimension is the number of variables contained in
        the data. It is the final goal to find the mean distribution for each 
        variable after bootstrapping. The second dimension is the number of
        'Configurations' -- the random values each variable is drawn from.

    NSamples : integer, (initialization method 1)
        The number of different bootstrap configurations which will be drawn
        for the number of initial configurations. This determines the second
        dimension of the data member 'self.samples'. The first one remains 
        NVars.

    NSize : integer, (initialization method 1)
        The size of each bootstrap configuration. This dimension will eventually
        be used to compute the mean of the bootstrap samples.
        Note that it is advised to have NSize smaller than the number of bins.

    NBinSize : integer (initialization method 1 and 2)
        The size of the Bins which is applied before drawing bootstrap samples.
        Data values are averaged in bins according to
        'self.data[i] = mean(data[i:i+NBinSize])'.
        This can reduce auto correlations within the data.

    indices : two-dimensional ndarray (NSamples x NSize), int
              (initialization method 2)
        The random indices for computing the bootstrap distribution of the mean.
        They are drawn from an uniform distribution 'U(0, NBins-1)' -- 
        corresponding to indices for the binned data.

    h5Info: dictionary with values for keys 'fileName' and 'groupName'
            (initialization method 3)
        Reads HDF5 files which where exported by 'self.exportHDF5'.
        The fileName must point to a valid HDF5 file while the groupName
        must point group conainting the exported 'bootstrap' group.
        This reads the indices and parameters contained in the HDF5 file.

    See Also
    --------
    'self.exportHDF5', 'self.samples'

    Notes
    -----
    This class is a wrapper for a C++ file. Thus, the routines are more 
    efficient than numpy routines (tested on my machine only).

    Examples
    --------

    Parameter initialization:

    >>> data = np.random.normal(size=[128, 2000])
    >>> bs1  = boot.Bootstrapper(
    >>>     data,
    >>>     NSamples=1000,
    >>>     NSize=400,
    >>>     NBinSize=5,
    >>> )
    >>> bs1
    Bootstrapper(NSamples=1000, NSize=400, NBinSize=5, NConfigs=2000, 
    NVars=128, NBins=400)

    Indices initialization:

    >>> bs2  = boot.Bootstrapper(data, indices=bs1.indices)
    >>> print(bs2, bs2 == bs1)
    Bootstrapper(NSamples=1000, NSize=400, NBinSize=5, NConfigs=2000, 
    NVars=128, NBins=400), True

    H5File initialization:

    >>> h5Info = {'fileName': 'bootstrap.h5', 'groupName': 'ensemble1'}
    >>> bs1.exportHDF5(**h5Info)
    >>> bs3 = boot.Bootstrapper(data, h5Info=h5Info)
    >>> print(bs3, bs3 == bs1)
    Bootstrapper(NSamples=1000, NSize=400, NBinSize=5, NConfigs=2000, 
    NVars=128, NBins=400), True
    """
    # Check whether input is given by HDF5 file
    if not(h5Info is None):
      # Check if input is correct
      fileName  = h5Info.get("fileName")
      groupName = h5Info.get("groupName")
      if fileName is None or groupName is None:
        raise KeyError(
          "To load a 'Bootstrapper' from a HDF5 file, you must specify the keys"
          + " 'fileName' and 'groupName'."
        )

      # Open group
      bootAddress = os.path.join("/", groupName, "bootstrap")
      with h5py.File(fileName, "r") as f:
        bootGroup = f.get(bootAddress)
        # Check wether group exists
        if bootGroup is None:
          raise KeyError("Could not open group: {}".format(bootAddress))

        # Read file
        ## Read NBinSize
        NBinSize = bootGroup.get("NBinSize").value
        ## Read indices
        indices = bootGroup.get("indices").value

    # initialize the C++ object
    # Check data type
    data = np.array(data)
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
    ## The number of configurations in the ensemble. 
    ## This is the first dimension of the input array.
    self.NConfigs = self.boot.NConfigs
    ## The number of variables in the ensemble.
    ## Second dimension of the input array.
    self.NVars    = self.boot.NVars
    ## The number of bins given by 'NConfigs/NBinSize'.
    ## In case 'NConfigs % NBinSize != 0', the remainder is skipped at the 
    #  beginning of the input data array.
    self.NBins    = self.boot.NBins
    ## The binned data of size 'NVars x NBins'.
    # Note that this is not the input data.
    self.data     = self.boot.data
    ## The bootstrap indicies of size 'NSamples x NSize'.
    self.indices  = self.boot.indices
    ## Returns the mean of the 'data'.
    # Note: This mean is also equal to the mean of the input data modulo the 
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
    """
    Return the bootstrap samples.

    Returns
    ----------
    out : ndarray
        The bootstrap samples of size 'self.NVars x self.NSamples'.
        This routines uses 'self.indices' to reshape 'self.data' before 
        averaging. The averaged out dimension is 'self.NSize'.

    Notes
    -----
    This is the most expensive computation. The output array is not stored
    within this class. Make sure, if you want to use it, to store it elsewhere.

    See Also
    --------
    'samples'
    """
    return self.boot._getSamples()

  #------------------
  @property
  def samples(self):
    """
    Return the bootstrap samples.

    Returns
    ----------
    out : ndarray
        The bootstrap samples of size 'self.NVars x self.NSamples'.
        This routines uses 'self.indices' to reshape 'self.data' before 
        averaging. The averaged out dimension is 'self.NSize'.

    Notes
    -----
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
    """Returns str(self)"""
    return str(self)

  #------------------
  def __eq__(self, other):
    """
    Compares wheter the other has the same input parameter and data.

    Parameters
    ----------
    other : arbitrary
        If instance of 'Bootstrapper' checks 'self.parameters', 'self.indices' 
        and 'self.data',  else returns 'False'.

    Returns
    ----------
    out : boolean
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
    Exports the bootstrap data to the HDF5 file 'fileName'.

    It exports the 'parameters' as well as the indices to the group
    >>> groupAddress = '/' + groupName + '/bootstrap'

    Parameters
    ----------
    fileName : string
        Address pointing to the export HDF5 file. If this file exists,
        the routine appends, otherwise it writes.

    groupName : string, optional
        Group name (can include subgroups) to write to. If this group already 
        exists in the file, it opens the group. Otherwise, this routine will
        create the group. If this group also includes a group 'bootstrap', this
        routines raises an error.

    writeSamples : boolean, optional
        If set to true, also exports the computed samples to the hdf5 file.

    See Also
    --------
    Bootstrapper initialization

    Notes
    -----
    This routine does not store the initial data. For full reproducability,
    the data must be exported elsewhere.

    Examples
    --------
    >>> h5Info = {'fileName': 'bootstrap.h5', 'groupName': 'ensemble1'}
    >>> bs1.exportHDF5(**h5Info)
    >>> bs2 = boot.Bootstrapper(data, h5Info=h5Info)
    >>> bs2 == bs1
    True
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
        raise KeyError(
          "Group >bootstrap< already exist for base group >{}<. Stop writing".format(
            groupName
          ),
          groupName
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