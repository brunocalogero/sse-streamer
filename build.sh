#!/bin/bash

set -eux

# This is the Python version of the build script.
# The create-release script will move this to the top-level directory when
# creating its zip file.

npm ci
pushd ./backend-py
    docker compose pull || docker-compose pull
    docker compose build || docker-compose build
popd
