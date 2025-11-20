#!/usr/bin/env python3
"""Map 5"""
import sys

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    fields = line.split("\t")

    if len(fields) == 4:
        # TF-IDF
        term, docid, tf, idf = fields
        print(f"{term}\t{docid}\t{tf}\t{idf}")

    elif len(fields) == 2:
        # Norm
        docid, norm = fields
        print(f"{docid}\t{norm}")
