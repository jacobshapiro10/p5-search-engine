#!/usr/bin/env python3
"""Reduce 0 to sum up HTML document counts."""
import sys

total = 0
for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    total += int(line)

print(total)
