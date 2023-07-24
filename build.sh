#!/bin/bash
set -e

docker build --rm \
    -t crud_container \
    crud_image .
