#!/bin/bash

set -eux

# This is the Python version of the start script.
# The create-release script will move this to the top-level directory when
# creating its zip file.

npx concurrently 'react-scripts start' '(cd ./backend-py && (docker compose up || docker-compose up))'
