#!/bin/sh
# This script demonstrates how to use gxenv in general shell script.
# Create env named `env` before running this.

INTERP=$(gxenv which env python3)

${INTERP} <<EOF
import sys
print("Hello world!")
print("sys.argv =", sys.argv)
print("sys.executable =", sys.executable)
EOF

