#!/usr/bin/env bash
source ./env

if [[ ! -d "$BASE/build-vm/${TEST_IDENTIFIER}" ]]; then
   ./test-setup.sh || exit 1
fi

pushd "$BASE/sdk/android-sdk-r${SDK_REV}" > /dev/null

# TODO: Figure out an appropriate port number.
PORT=5554

# Boot the emulator, wait for it.
./tools/emulator -avd "${ANDROID_VM_NAME}-${TEST_IDENTIFIER}" -port "${PORT}" -no-snapshot-save ${ANDROID_EMULATOR_OPTIONS} &
./platform-tools/adb -s "emulator-${PORT}" wait-for-device

# Copy the files over.
./platform-tools/adb -s "emulator-${PORT}" push "${ANDROID_PREFIX}/${BUILD_IDENTIFIER}" "${ANDROID_EMULATOR_TESTDIR}"
# Run the tests!
./platform-tools/adb -s "emulator-${PORT}" shell <<-EOF
	cd "${ANDROID_EMULATOR_TESTDIR}"
	bin/python3.3 -m test
	exit
EOF
# Stop the emulator.
./platform-tools/adb -s "emulator-${PORT}" emu kill

popd > /dev/null
