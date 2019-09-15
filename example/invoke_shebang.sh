#!/usr/bin/gxenv run env python3
# This script demonstrates how to use gxenv via shebang.
# Create env named `env` before running this.

# To make gxenv verbose:
#!/usr/bin/gxenv -v run env python3

import sys


print("Hello world!")
print("sys.argv =", sys.argv)
print("sys.executable =", sys.executable)
