#!/usr/bin/env python3
"""Map 5 to partition TF-IDF and norm records by segment ID."""
import sys

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue

    fields = line.split("\t")

    # TF-IDF record: term docid tf idf
    if len(fields) == 4:
        term, docid, tf, idf = fields
        segment_id = int(docid) % 3
        # key = segment_id
        print(f"{segment_id}\t{term}\t{docid}\t{tf}\t{idf}")

    # Norm record: docid norm
    elif len(fields) == 2:
        docid, norm = fields
        segment_id = int(docid) % 3
        # key = segment_id
        print(f"{segment_id}\t{docid}\t{norm}")
