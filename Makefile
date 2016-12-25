## Setup.

PYTHON=python3.7

all: build

## Building.

build:
	$(PYTHON) -m pybuild

## Cleaning.

clean:
	$(PYTHON) -m pybuild.clean
