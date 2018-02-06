# bootstrap-statistics
Python wrapper for C++ routine which computes bootstrap distributions of the mean for randomly distributed variables.
This module provides unittests for all routines.

## Content
1. [Description](#Description)
2. [Getting started](#Getting-started)
    1. [Perquisites](#Perquisites)
    2. [Installing](#Installing)
    3. [Running the tests](#Running-the-tests)
3. [Usage](#Usage)
4. [Authors](#Authors)
5. [License](#License)

## <a name="Description"></a>Description
The objective of this module to estimate the mean value and its uncertainty of randomly distributed variables.
The specific example for which this routine was created are so-called correlator files coming from Hybrid Monte Carlo (HMC) algorithms.
For more details, I refer to https://arxiv.org/abs/hep-lat/0506036.

Assume the random data is stored in an array `data` of shape `NVars x NConfigurations`.
It is the goal to estimate the mean value of data for each variable along the configuration axis.
The algorithm first averages over the configuration axis and creates bins of size `NBinSize`
```python
binnedData[nVar, nBin] = mean(data[nVar, nBin*NBinSize : (nBin+1)*NBinSize])
```
In case the number of configurations is not divisible by the bin size, the remaining configurations are thrown away at the beginning of the array (see, e.g., the unittests).

Next the routine computes uniformly distributed indices in the interval from `0 .. NBins` of shape `NSamples x NSize` with possible repetitions.
The integer `NSize` is an input for the routine.
It is usually equal to the number of bins `NSize = NBins` -- it should not be too small but also not too large (to not allow too many redraws).

Finally, the samples are computed according to
```python
samples = mean(binnedData[:, indices], axis=2)
```
Note that all of this is handled in C++ in order to optimize perfomance and memory usage.

## <a name="Getting-started"></a>Getting started

### <a name="Perquisites"></a>Perquisites

Python Modules:
 - `numpy`
 - `cython`
 - `h5py`

Both will be automatically installed when pip-installing the package.

Also, a standard 17 (`-std=c++17`) compatible C++ compiler is required.

### <a name="Installing"></a>Installing

This module can be pip installed by typing either
```bash
pip install -e .
```
in the root directory.
This installation tracks updates of the repository (symlinks).
In case you do not want this but still have a pip install, just type
```bash
pip install .
```

For the basic compilation type 
```bash
make build
```
in the root directory.
You have to export or copy the resulting `.so` file to the directory of choice in case you use this installation procedure.

To see if the C++ files compile as desired, run
```bash
make cTest
```

The installation using all these commands assumes that your basic compiler is compatible with the `c++17` standard.
If this is not the case export a compatible compiler beforehand, e.g.,
```bash
export CC=clang; export CXX=clang++; pip install -e .
```
To figure out if your compiler is sufficient, try to compile the C++ base files in `bootstats/cFiles`.

### <a name="Uninstalling"></a>Uninstalling
In case of a pip install
```bash
pip uninstall bootstrap-statistics
```
In case of `make build` install, type
```bash
make clean
```
in root directory.

### <a name="Running-the-tests"></a>Running the tests
Running test through `setup.py`
```bash
python3 setup.py test
```
or through pythons `unittest` module (once installed)
```bash
python -m -v "unittest" tests/testBootstats.py
```
Make sure that the python version matches the installation version.


## <a name="Usage"></a>Usage

The `Bootstrapper` class can be initiated with real and complex data.
On initialization, random indices will be created.
The bootstrap samples can be accessed through the `samples` member of the class.
The computation of the samples is executed once (and the only time) the first time the member is accessed.
It is not really important which dimension `nd > 2` the `data` array has as long as the last entry corresponds to the random entries of the variable.

Last but not least, bootstrap indices (and also samples) can be exported to and read from `HDF5` files.

### Importing the basic module
```python
import bootstats
```

### Creating a Bootstrapper instance
Creation by parameters
```Python
data = np.random.random(size=[128, 1000])
bs1  = bootstats.Bootstrapper(data, NSamples=2000, NBinSize=5, NSize=200)
bs1.samples.shape # = 128 x 2000
```

Creation by indices
```Python
bs2 = bootstats.Bootstrapper(data, bs1.indices, NBinSize=5)
bs1 == bs2 # = True
```

Creation by HDF5 file
```Python
h5Info={"fileName": "test.h5", "groupName": "testGroup"}
bs1.exportHDF5(**h5Info)
bs3 = boot.Bootstrapper(data, h5Info=h5Info)
bs1 == bs3 # = True
```

For more example see the `examples/` directory.

## <a name="Authors"></a>Authors
* **Christopher Körber**


## <a name="License"></a>License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

