PYTHON?=python

all:
	$(PYTHON) -m pybuild

clean:
	$(PYTHON) -m pybuild.clean

test:
	$(PYTHON) -m pybuild.check_cpython_modules

send:
	$(PYTHON) -m pybuild.send

.PHONY: all clean test send
