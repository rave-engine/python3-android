#!/bin/bash
gpg --debug ipc --keyserver hkp://ipv4.pool.sks-keyservers.net --recv-keys $(python3.8 -m pybuild.pgp_keys)
