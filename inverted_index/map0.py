#!/usr/bin/env python3
"""Map function to identify HTML documents."""
import sys

for line in sys.stdin:
    if "<!DOCTYPE html>" in line:
        print(1)
