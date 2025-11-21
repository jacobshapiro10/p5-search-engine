#!/bin/bash
#
# Example of how to chain MapReduce jobs together.  The output of one
# job is the input to the next.
#
# Madoop options
# -input <directory>                            # Input directory
# -output <directory>                           # Output directory
# -mapper <exec_name>                           # Mapper executable
# -reducer <exec_name>                          # Reducer executable
# -partitioner <exec_name>                      # Optional: Partitioner executable

# Stop on errors
# See https://vaneyckt.io/posts/safer_bash_scripts_with_set_euxo_pipefail/
set -Eeuo pipefail

# Optional input directory argument
PIPELINE_INPUT=crawl
if [ -n "${1-}" ]; then
  PIPELINE_INPUT="$1"
fi

set -x   # Print commands

# Clean old directories
rm -rf output output[0-9] combined_input_5 total_document_count.txt

############################################
# Job 0 — Count Documents
############################################
madoop \
  -input ${PIPELINE_INPUT} \
  -output output0 \
  -mapper ./map0.py \
  -reducer ./reduce0.py

# Save doc count (used by Reduce 3)
cp output0/part-00000 total_document_count.txt


############################################
# Job 1 — HTML Parsing → docid \t text
############################################
madoop \
  -input ${PIPELINE_INPUT} \
  -output output1 \
  -mapper ./map1.py \
  -reducer ./reduce1.py


############################################
# Job 2 — term \t docid \t tf_partial
############################################
madoop \
  -input output1 \
  -output output2 \
  -mapper ./map2.py \
  -reducer ./reduce2.py


############################################
# Job 3 — Add IDF → term \t docid \t tf \t idf
############################################
madoop \
  -input output2 \
  -output output3 \
  -mapper ./map3.py \
  -reducer ./reduce3.py


############################################
# Job 4 — Compute doc norms → docid \t norm
############################################
madoop \
  -input output3 \
  -output output4 \
  -mapper ./map4.py \
  -reducer ./reduce4.py
  

############################################
# Job 5 — Needs output3 + output4
# MUST combine directories manually
############################################
rm -rf combined_input_5
mkdir combined_input_5

# Copy output3 files as-is
rsync -a output3/ combined_input_5/

# Copy output4 files with a prefix to avoid name collision
for file in output4/part-*; do
  basename=$(basename "$file")
  cp "$file" "combined_input_5/norm_${basename}"
done

madoop \
  -input combined_input_5 \
  -output output \
  -mapper ./map5.py \
  -reducer ./reduce5.py \
  -partitioner ./partition.py \
  -numReduceTasks 3


echo "Pipeline complete!"