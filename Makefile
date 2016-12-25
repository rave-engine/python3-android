PYTHON?=python3.7

all:
	$(PYTHON) -m pybuild

clean:
	$(PYTHON) -m pybuild.clean

test:
	$(PYTHON) -m pybuild.check_cpython_modules

.PHONY: all clean test
