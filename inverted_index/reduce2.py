#!/usr/bin/env python3
"""Reduce 2 to sum term frequencies per (term, docid)."""
import sys

# Input format:
# term<TAB>docid<TAB>1

current_key = None
CURRENT_SUM = 0

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue

    term, doc_id, count_str = line.split("\t")
    key = (term, doc_id)
    count = int(count_str)

    if key != current_key:
        # Output previous term/docid
        if current_key is not None:
            print(f"{current_key[0]}\t{current_key[1]}\t{CURRENT_SUM}")

        # reset for new key
        current_key = key
        CURRENT_SUM = 0

    CURRENT_SUM += count

# Final flush
if current_key is not None:
    print(f"{current_key[0]}\t{current_key[1]}\t{CURRENT_SUM}")
