## Setup.

all: build

# Get configuration.
mk/env.mk: env
	@bash --noprofile --norc -c 'source ./env; set -o posix; set' | egrep '^(ANDROID|SDK|NDK|BUILD|TEST|PYTHON)_' > $@
-include mk/env.mk

# A formula.
define formula
$1: $1-$2

$1-$2: $3
	$$(info Checking $1 $2 sources...)
	@mk/get_source.sh $1
ifeq ("$$(wildcard build/.built-$(BUILD_IDENTIFIER)/$1-$2)","")
	$$(info Building $1 $2...)
	@bash --noprofile --norc mk/build_single.sh $1 $2
	mkdir -p build/.built-$(BUILD_IDENTIFIER)
	@touch build/.built-$(BUILD_IDENTIFIER)/$1-$2
endif
endef


## Building.

build: python_modules python

# Main Python.
$(eval $(call formula,python,hg))

# Optional Python modules.
python_modules: android-support $(foreach mod,$(subst ',,$(PYTHON_OPTIONAL_MODULES)),python_$(mod))

$(eval $(call formula,android-support,))

# Python lzma support.
$(eval $(call formula,xz,5.2.1))
python_lzma: xz

# Python bzip2 support.
$(eval $(call formula,bzip2,1.0.6))
python_bz2: bzip2

# Python readline support.
$(eval $(call formula,readline,6.3))
python_readline: readline

# Python SSL support.
$(eval $(call formula,openssl,1.0.2g))
python_ssl: openssl

# Python curses support.
$(eval $(call formula,ncurses,6.0))
python_curses: ncurses

# Python SQLite support.
$(eval $(call formula,sqlite,3.12.2))
python_sqlite3: sqlite

# Python (g)dbm support.
$(eval $(call formula,gdbm,1.11))
python_gdbm: gdbm


## Cleaning.

clean: clean_generated clean_builds
	@rm -rf "$(ANDROID_TEST_PREFIX)"
	@rm -rf "$(ANDROID_TOOL_PREFIX)"

clean_generated:
	@find ./src -mindepth 1 -maxdepth 1 -type d -exec rm -rf "{}" \;

clean_builds:
	@rm -rf "$(ANDROID_PREFIX)"


## Testing.

test: test_setup
	@bash --noprofile --norc mk/test.sh

test_setup:
ifeq ("$(wildcard build-vm/$(TEST_IDENTIFIER))","")
	@bash --noprofile --norc mk/test_setup.sh
endif
