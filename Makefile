## Setup.

all: build

# Get configuration.
mk/env.mk: env
	@bash --noprofile --norc -c 'source ./env; set -o posix; set' | sed -e "s#'##g" | egrep '^(ANDROID|NDK|BUILD|PYTHON)_' > $@
include mk/env.mk

PYTHON_MODULES=

# A formula.
define formula
PYTHON_MODULES=$(PYTHON_MODULES) $1

$1: $2
	$$(info Checking $1 sources...)
	@mk/get_source.sh $1
ifeq ("$$(wildcard build/.built-$(BUILD_IDENTIFIER)/$1)","")
	$$(info Building $1...)
	@bash --noprofile --norc mk/build_single.sh $1
	mkdir -p build/.built-$(BUILD_IDENTIFIER)
	@touch build/.built-$(BUILD_IDENTIFIER)/$1
endif
endef


## Building.

build: python_modules python

# Main Python.
$(eval $(call formula,python))

# Optional Python modules.
python_modules: $(PYTHON_OPTIONAL_MODULES)

# Python lzma support.
$(eval $(call formula,xz))

# Python bzip2 support.
$(eval $(call formula,bzip2))

# Python readline support.
$(eval $(call formula,readline))

# Python SSL support.
$(eval $(call formula,openssl))

# Python curses support.
$(eval $(call formula,ncurses))

# Python SQLite support.
$(eval $(call formula,sqlite))

# Python (g)dbm support.
$(eval $(call formula,gdbm))

# Python ctypes/libffi support
$(eval $(call formula,libffi))


## Cleaning.

clean: clean_generated clean_builds

clean_generated:
	mods="$(PYTHON_MODULES)" && \
	for mod in $${mods[@]} ; do \
		bash --norc --noprofile -e mk/clean_single.sh $$mod ; \
	done

clean_builds:
	@rm -rf "$(ANDROID_PREFIX)"
