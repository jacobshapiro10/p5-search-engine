#!/usr/bin/env python3
"""Reduce 5"""
import sys
from collections import defaultdict

norms = {}
postings = defaultdict(list)

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue

    fields = line.split("\t")

    # Norm record: segment_id<tab>docid<tab>norm
    if len(fields) == 3:
        segment_id, docid, norm = fields
        norms[docid] = norm

    # TF-IDF record: segment_id<tab>term<tab>docid<tab>tf<tab>idf
    elif len(fields) == 5:
        segment_id, term, docid, tf, idf = fields
        postings[term].append((docid, tf, idf))

# Output in term-sorted order
for term in sorted(postings.keys()):
    _, _, idf = postings[term][0]
    print(f"{term} {idf}", end="")
    
    for docid, tf, _ in sorted(postings[term], key=lambda x: x[0]):
        norm = norms.get(docid, "0")
        print(f" {docid} {tf} {norm}", end="")
    
    print()