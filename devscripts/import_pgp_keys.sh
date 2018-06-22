#!/bin/bash
cat devscripts/pgp-keys/*.asc | gpg --import
