#!/bin/bash

## Merged all the bedpe files to create one big contact file.
## Took help from CHATGPT

# Configurable parameters
NAMES_FILE="final_k62_uniq_cell_name.txt"
BIGFILE="merged_k62_all.txt"
CHUNK_LINES=4000     # Adjust this if needed
CHUNKS_DIR="name_chunks"
OUTPUT_DIR="matched_output"
JOBS=10              # Number of parallel jobs (adjust to your CPU core count)

# Create working directories
mkdir -p "$CHUNKS_DIR" "$OUTPUT_DIR"

# Step 1: Split names.txt into chunks of $CHUNK_LINES
split -l "$CHUNK_LINES" "$NAMES_FILE" "$CHUNKS_DIR/names_chunk_"

# Step 2: Process each chunk in parallel
process_chunk() {
    local chunk_file="$1"
    local chunk_name
    chunk_name=$(basename "$chunk_file")

    awk -v namefile="$chunk_file" -v outdir="$OUTPUT_DIR" '
    BEGIN {
        while ((getline < namefile) > 0) {
            names[$0] = 1
        }
    }
    {
        if ($7 in names) {
            print >> (outdir "/" $7 ".txt")
            close(outdir "/" $7 ".txt")
        }
    }
    ' "$BIGFILE"
}

export -f process_chunk
export BIGFILE OUTPUT_DIR

# Step 3: Run in parallel using xargs
find "$CHUNKS_DIR" -type f | xargs -n1 -P"$JOBS" -I{} bash -c 'process_chunk "$@"' _ {}

echo "Jobs Completed. Matched files are in: $OUTPUT_DIR/"
