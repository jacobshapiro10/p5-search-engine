#!/usr/bin/env python3
"""Reduce 5"""
import sys
from collections import defaultdict

# norms[docid] = norm_value
norms = {}

# postings[term] = list of (docid, tf, idf)
postings = defaultdict(list)

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue

    fields = line.split("\t")

    # Norm record: docid norm
    if len(fields) == 3:
        _, docid, norm = fields
        norms[docid] = norm

    # TF-IDF record: term docid tf idf
    elif len(fields) == 5:
        _, term, docid, tf, idf = fields
        postings[term].append((docid, tf, idf))

# Output in term-sorted order
for term in sorted(postings.keys()):
    # All postings for a term share the same idf
    _, _, idf = postings[term][0]

    # Start line: term + idf
    print(f"{term} {idf}", end="")

    # Sort postings by docid (string lexicographic)
    for docid, tf, _ in sorted(postings[term], key=lambda x: x[0]):
        norm = norms.get(docid, "0")
        # Add: docid tf norm
        print(f" {docid} {tf} {norm}", end="")

    print()  # newline after each term
