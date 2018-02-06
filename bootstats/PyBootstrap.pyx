from libcpp.vector cimport vector
import numpy as np

cdef extern from "complex.h":
    double complex cexp(double complex)

#-----------------------------------------------------------
# -----------------------Bootstrapper---------------------
#-----------------------------------------------------------
cdef extern from "cFiles/Bootstrap.hpp":
  cdef cppclass Bootstrapper[T]:
    Bootstrapper(
      const vector[vector[T]] &data, 
      const size_t NSamples,
      const size_t NSize,
      const size_t NBinSize
    ) except +
    Bootstrapper(
      const vector[vector[T]] &data, 
      const vector[vector[size_t]] &indices,
      const size_t NBinSize
    ) except +


    const size_t getNSamples() const;
    const size_t getNSize()    const;
    const size_t getNBinSize() const;
    const size_t getNConfigs() const;
    const size_t getNVars()    const;
    const size_t getNBins()    const;

    const vector[vector[T]]      &getData()    const;
    const vector[vector[size_t]] &getIndices() const;

    const vector[T] &getMean() const;
    const vector[vector[T]] &getSamples() const;

    const vector[vector[T]] &getCov() const;
    const vector[vector[T]] &getCov(vector[vector[T]]) const;

#--------------- python version-----------------------------
cdef class DoubleBootstrapper(object):
  cdef Bootstrapper[double] *ptr
  #------------
  def __cinit__(
    self,
    vector[vector[double]] data,
    NSamples=None,
    NSize=None,
    NBinSize=None,
    indices=None,
  ):
    if not(NSamples is None) and not(NSize is None) and not(NBinSize is None):
      self.ptr = new Bootstrapper[double](
        data, NSamples, NSize, NBinSize
      )
    elif not(indices is None) and not(NBinSize is None):
      self.ptr = new Bootstrapper[double](
        data, indices, NBinSize
      )
    else:
      raise ValueError(
        "Either construct Bootstrapper from [data, NSampels, NSize, NBinSize]"+
        " or [data, indices, NBinSize]."
      )
  #------------
  @property
  def NSamples(self):
    return  self.ptr.getNSamples()
  @property
  def NSize(self):
    return  self.ptr.getNSize()
  @property
  def NBinSize(self):
    return  self.ptr.getNBinSize()
  @property
  def NConfigs(self):
    return  self.ptr.getNConfigs()
  @property
  def NVars(self):
    return  self.ptr.getNVars()
  @property
  def NBins(self):
    return  self.ptr.getNBins()
  @property
  def data(self):
    return  np.array(self.ptr.getData())
  @property
  def indices(self):
    return  np.array(self.ptr.getIndices())
  @property
  def mean(self):
    return np.array(self.ptr.getMean())
  #------------
  def __str__(self):
    return "ComplexBootstrapper({NSamples},{NSize},{NBinSize})".format(
      NSamples=self.NSamples, NSize=self.NSize, NBinSize=self.NBinSize
    )
  def __repr__(self):
    return str(self)
  #------------
  def _getSamples(self):
    return np.array(self.ptr.getSamples())
  #------------
  def getCov(self, samples=None):
    if samples is None:
      return np.array(self.ptr.getCov())
    else:
      return np.array(self.ptr.getCov(samples))

#--------------- python version-----------------------------
cdef class ComplexBootstrapper(object):
  cdef Bootstrapper[complex] *ptr
  #------------
  def __cinit__(
    self,
    vector[vector[complex]] data, 
    NSamples=None,
    NSize=None,
    NBinSize=None,
    indices=None,
  ):
    if not(NSamples is None) and not(NSize is None) and not(NBinSize is None):
      self.ptr = new Bootstrapper[complex](
        data, NSamples, NSize, NBinSize
      )
    elif not(indices is None) and not(NBinSize is None):
      self.ptr = new Bootstrapper[complex](
        data, indices, NBinSize
      )
    else:
      raise ValueError(
        "Either construct Bootstrapper from [data, NSampels, NSize, NBinSize]"+
        " or [data, indices, NBinSize]."
      )
  #------------
  @property
  def NSamples(self):
    return  self.ptr.getNSamples()
  @property
  def NSize(self):
    return  self.ptr.getNSize()
  @property
  def NBinSize(self):
    return  self.ptr.getNBinSize()
  @property
  def NConfigs(self):
    return  self.ptr.getNConfigs()
  @property
  def NVars(self):
    return  self.ptr.getNVars()
  @property
  def NBins(self):
    return  self.ptr.getNBins()
  @property
  def data(self):
    return  np.array(self.ptr.getData())
  @property
  def indices(self):
    return  np.array(self.ptr.getIndices())
  @property
  def mean(self):
    return np.array(self.ptr.getMean())
  #------------
  def __str__(self):
    return "ComplexBootstrapper({NSamples},{NSize},{NBinSize})".format(
      NSamples=self.NSamples, NSize=self.NSize, NBinSize=self.NBinSize
    )
  def __repr__(self):
    return str(self)
  #------------
  def _getSamples(self):
    return np.array(self.ptr.getSamples())
