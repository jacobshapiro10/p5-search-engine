#!/usr/bin/env python3
"""Map 4"""
import sys

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    term, doc_id, term_frequency, idf = line.split("\t")
    term_frequency = float(term_frequency)
    idf = float(idf)
    weight = (term_frequency * idf) * (term_frequency * idf)
    
    # Emit for norm calculation
    print(f"{doc_id}\t{weight}")
    
    # Pass through the TF-IDF record unchanged
    print(line)