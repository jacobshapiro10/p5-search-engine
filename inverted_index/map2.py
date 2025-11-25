#!/usr/bin/env python3
"""Map to create (term, docid, 1) triples."""
import sys
import re

stopwords = set()
with open("stopwords.txt", encoding="utf-8") as f:
    for w in f:
        stopwords.add(w.strip())


for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    doc_id, content = line.split("\t", 1)
    content = re.sub(r"[^a-zA-Z0-9 ]+", "", content)
    content = content.casefold()
    words = content.split()
    for word in words:
        if word not in stopwords and word != "":
            print(f"{word}\t{doc_id}\t1")
