## Setup.

all: build

# Get configuration.
mk/env.mk: env
	@bash --noprofile --norc -c 'source ./env; set -o posix; set' | egrep '^(ANDROID|SDK|NDK|BUILD|TEST|PYTHON)_' > $@
-include mk/env.mk

# A formula.
define formula
$1: $1-$2

$1-$2: ndk $3
	$$(info Checking $1 $2 sources...)
	@wget --no-check-certificate -nv -N -P "src/" -i "mk/$1/$2/sources.txt"
ifeq ("$$(wildcard build/.built-$(BUILD_IDENTIFIER)/$1-$2)","")
	$$(info Building $1 $2...)
	@bash --noprofile --norc mk/build_single.sh $1 $2
	@touch build/.built-$(BUILD_IDENTIFIER)/$1-$2
endif
endef


## Building.

build: python_modules python-3.3.3

# Main Python.
$(eval $(call formula,python,3.3.3))

# Optional Python modules.
python_modules: $(foreach mod,$(subst ',,$(PYTHON_OPTIONAL_MODULES)),python_$(mod))

# Python lzma support.
$(eval $(call formula,xz,5.0.5))
python_lzma: xz

# Python bzip2 support.
$(eval $(call formula,bzip2,1.0.6))
python_bz2: bzip2

# Python readline support.
$(eval $(call formula,readline,6.3))
python_readline: readline

# Python SSL support.
$(eval $(call formula,openssl,1.0.1h))
python_ssl: openssl


# Android NDK.
ndk:
	$(info Checking NDK sources...)
	@wget -nv -N -P "sdk/" $(shell bash mk/ndk_source.sh)
ifeq ("$(wildcard build/.built-ndk-$(BUILD_IDENTIFIER))","")
	$(info Preparing NDK toolchain...)
	@bash --noprofile --norc mk/build_ndk.sh
	@touch build/.built-ndk-$(BUILD_IDENTIFIER)
endif


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
