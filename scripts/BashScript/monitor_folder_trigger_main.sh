#!/bin/bash

# Directory to monitor
INPUT_DIR="/path/to/input/directory"
OUTPUT_DIR="/path/to/output/directory"

# Function to trigger the main.py script
process_file() {
    local input_file="$1"
    echo "New file detected: $input_file"
    
    # Run the main.py script with the new DXF file
    python3 /path/to/main.py "$input_file" --output_dir "$OUTPUT_DIR"
    
    if [ $? -eq 0 ]; then
        echo "File processed successfully: $input_file"
    else
        echo "Failed to process file: $input_file"
    fi
}

# Monitor the directory for new DXF files
inotifywait -m -e close_write --format '%w%f' "$INPUT_DIR" | while read NEW_FILE
do
    # Check if the new file has a .dxf extension
    if [[ "$NEW_FILE" == *.dxf ]]; then
        process_file "$NEW_FILE"
    fi
done
