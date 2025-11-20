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
    if len(fields) == 2:
        docid, norm = fields
        norms[docid] = norm

    # TF-IDF record: term docid tf idf
    elif len(fields) == 4:
        term, docid, tf, idf = fields
        postings[term].append((docid, tf, idf))

# Output in term-sorted order
for term in sorted(postings.keys()):
    # All TF-IDF entries for the term have the same idf
    _, _, idf = postings[term][0]

    # Print: term <TAB> idf
    print(f"{term}\t{idf}", end="")

    # Sort postings by docid (string comparison)
    for docid, tf, _ in sorted(postings[term], key=lambda x: x[0]):
        norm = norms.get(docid, "0")
        # Append: <TAB> docid <TAB> tf <TAB> norm
        print(f"\t{docid}\t{tf}\t{norm}", end="")

    print()  # newline at end of term line
