#!/usr/bin/env python3
import sys
import math

# Read total document count
with open("total_document_count.txt") as f:
    N = int(f.read().strip())

current_term = None
docid_tf_list = []     # list of (docid, tf)

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue

    term, doc_id, tf_str = line.split("\t")
    tf = int(tf_str)

    # New term group
    if term != current_term:
        # Output previous term block
        if current_term is not None:
            DF = len(docid_tf_list)
            IDF = math.log10(N / DF)
            for d, t in docid_tf_list:
                print(f"{current_term}\t{d}\t{t}\t{IDF}")

        # Reset for new term
        current_term = term
        docid_tf_list = []

    docid_tf_list.append((doc_id, tf))

# Flush the last term
if current_term is not None:
    DF = len(docid_tf_list)
    IDF = math.log10(N / DF)
    for d, t in docid_tf_list:
        print(f"{current_term}\t{d}\t{t}\t{IDF}")
