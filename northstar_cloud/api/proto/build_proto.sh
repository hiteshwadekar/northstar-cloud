#!/usr/bin/env bash
set -e

# echo "The present working directory is `pwd`"
CDIR=$(dirname "$0")

# Generate python based proto API.
python -m grpc_tools.protoc -I. --python_out=$CDIR/. --grpc_python_out=$CDIR/. $CDIR/northstar.proto

