#!/usr/bin/env bash
source ./env

find "$BASE/src" -mindepth 1 -maxdepth 1 -type d -exec rm -rf "{}" \;
