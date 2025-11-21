#!/usr/bin/env python3
"""Reduce 4"""
import sys
import math

norm_factors = {}
tfidf_records = []

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    
    fields = line.split("\t")
    
    if len(fields) == 2:
        # It's a norm weight: docid<tab>weight
        doc_id, weight = fields
        weight = float(weight)
        if doc_id not in norm_factors:
            norm_factors[doc_id] = weight
        else:
            norm_factors[doc_id] += weight
    elif len(fields) == 4:
        # It's a TF-IDF record: term<tab>docid<tab>tf<tab>idf
        tfidf_records.append(line)

# Output norms
for doc_id, sum_of_squares in norm_factors.items():
    norm = math.sqrt(sum_of_squares)
    print(f"{doc_id}\t{norm}")

# Pass through TF-IDF records
for record in tfidf_records:
    print(record)