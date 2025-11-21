#!/usr/bin/env python3
import sys
import math
"""Reduce 4"""

my_dict = {}

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    doc_id, weight = line.split("\t")
    weight = float(weight)
    if doc_id not in my_dict:
        my_dict[doc_id] = weight
    else:
        my_dict[doc_id] += weight

for key, value in my_dict.items():
    my_dict[key] = math.sqrt(value)
    print(f"{key}\t{my_dict[key]}")