#!/usr/bin/env python3
import sys
import re


for line in sys.stdin:

    line = line.strip()
    if not line:
        continue
 
    doc_id, words = line.split("\t", 1)

    



        words = re.sub(r"[^a-zA-Z0-9 ]+", "", words)
        for word in words:
            word = word.str().casefold()
            print(f"{word}\t{doc_id}\t1")
