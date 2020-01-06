PYTHON?=python

all:
	$(PYTHON) -m pybuild

clean:
	rm -rvf build src/*

test:
	$(PYTHON) -m pybuild.check_cpython_modules

send:
	$(PYTHON) -m pybuild.send

.PHONY: all clean test send
