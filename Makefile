PIP=pip3
PYTHON=python3

# Directory which contains the C++ binaries
cFileDir=bootstats/cFiles

# All
.PHONY: all
all: build cTest

# Create a simple test file for the C++ Bootstrapper class
.PHONY: cTest
cTest:
	make -C $(cFileDir) test 

# Build the python module
.PHONY: build
build:
	$(PYTHON) setup.py build_ext --inplace

# Build a local pip module
.PHONY: local
local:
	$(PIP) install --user .

# Build a local pip module (tracks changes)
.PHONY: local-sym
local-sym:
	$(PIP) install --user -e .


# Build a local pip module (tracks changes)
.PHONY: test
test:
	$(PYTHON) setup.py test

# Clean
.PHONY: clean
clean:
	make -C $(cFileDir) clean
	$(RM) -r build/
	$(RM) *.so
	$(RM) -r *.egg-info
	$(RM) -r *.egg
	$(RM) *.pyc
	$(RM) -r __pycache__
