#!/usr/bin/env python3
import sys

total = 0
for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    total += int(line)

print(total)
