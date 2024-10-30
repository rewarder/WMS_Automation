#!/bin/bash

# Directory to monitor
INPUT_DIR="/home/debian/WMS_Upload/data"
PROCESSED_DIR="$INPUT_DIR/processed" 
OUTPUT_DIR="/home/wms/WMS_Automation/output"

# Function to trigger the main.py script
process_file() {
    local input_file="$1"
    echo "New file detected: $input_file"
    
    # Change working directory to WMS_upload
    cd /home/debian/WMS_Upload

    # Activate the virutal environment
    source ".venv/bin/activate"

    # Run the main.py script with the new DXF file
    python3 __init__.py --f "data/$input_file" --output_dir "$OUTPUT_DIR" --v
    
    if [ $? -eq 0 ]; then
        echo "File processed successfully: $input_file"
	# Move the original file to the processed directory
	mv "$input_file" "$PROCESSED_DIR/"
	if [ $? -eq 0 ]; then
		echo "File moved to processed directory: $PROCESSED_DIR/$(basename"$input_file")"
	else 
		echo "Failed to move file: $input_file"
	fi
    else
        echo "Failed to process file: $input_file"
    fi
}

# Monitor the directory for new DXF files
inotifywait -m -e close_write --format '%w%f' "$INPUT_DIR" | while read NEW_FILE
do
    # Check if the new file has a .dxf extension and does not start with 'inermediate_'
    if [[ "$NEW_FILE" == *.dxf && $(basename "$NEW_FILE") != intermediate_*.dxf ]]; then
        process_file "$NEW_FILE"
    fi
done
