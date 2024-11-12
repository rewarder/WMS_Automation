#!/bin/bash

# Directories
WATCH_DIR="/home/debian/WMS_Automation/output"
PROCESSED_DIR="$WATCH_DIR/processed"

# Create the processed directory if it doesn't exist
mkdir -p "$PROCESSED_DIR"

# Function to process files
process_files() {
    geojson_file="$1"
    json_file="$2"
    python3 /home/debian/WMS_Upload/src/tedawms/__main__.py --f "$geojson_file" --m "$json_file" -d
    
    # Move the processed files to the processed directory
    mv "$geojson_file" "$PROCESSED_DIR"
    mv "$json_file" "$PROCESSED_DIR"
}

# Monitor the directory for new files
inotifywait -m "$WATCH_DIR" -e create |
while read -r directory events filename; do
    if [[ "$filename" == modified_*_WGS84.geojson ]]; then
        # Introduce a delay to ensure the file is fully copied
        sleep 5  # Adjust the duration as needed
        
        # Find the corresponding JSON file
        base_name=$(echo "$filename" | sed 's/modified_\(.*\)_WGS84\.geojson/\1/')
        json_file=$(find "$WATCH_DIR" -name "*$base_name*.json" -print -quit)
        
        if [[ -f "$json_file" ]]; then
            geojson_file="$WATCH_DIR/$filename"
            process_files "$geojson_file" "$json_file"
        fi
    fi
done
