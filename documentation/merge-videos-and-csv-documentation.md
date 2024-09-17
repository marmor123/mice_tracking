# Merge Videos and CSV Files Script Documentation

## Overview

This Python script is designed to merge multiple video segments and their corresponding CSV files into a single video file and a single CSV file. It's particularly useful for reassembling video segments and tracking data that have been processed separately, such as those output by the `process_video_folder` script.

## Features

- Merges multiple MP4 video segments into a single MP4 file
- Combines multiple CSV files into a single CSV file
- Handles any number of input segments (not limited to 10)
- Sorts input files based on their numeric identifiers
- Preserves the original order of video segments and CSV data

## Requirements

- Python 3.x
- MoviePy library

## Installation

1. Ensure you have Python 3.x installed on your system.
2. Install the required library using pip:

   ```
   pip install moviepy
   ```

3. Download the `merge_videos_and_csv.py` script to your local machine.

## Usage

Run the script from the command line with the following syntax:

```
python merge_videos_and_csv.py <input_folder> <output_video> <output_csv>
```

### Arguments:

- `<input_folder>`: Path to the folder containing the processed video segments and CSV files
- `<output_video>`: Path and filename for the output merged video file (should end with .mp4)
- `<output_csv>`: Path and filename for the output merged CSV file (should end with .csv)

### Example:

```
python merge_videos_and_csv.py /path/to/processed/segments /path/to/merged_video.mp4 /path/to/merged_data.csv
```

## Input File Requirements

- Video files should end with '_output.mp4'
- CSV files should end with '_output.csv'
- Files should contain numeric identifiers in their names for proper sorting

## Functions

### `sort_files(files)`

Sorts the input files based on the numeric part of their filenames.

- **Parameters**: 
  - `files`: List of filenames to sort
- **Returns**: Sorted list of filenames

### `merge_videos(input_folder, output_video)`

Merges all video segments in the input folder into a single video file.

- **Parameters**:
  - `input_folder`: Path to the folder containing video segments
  - `output_video`: Path and filename for the output merged video

### `merge_csv_files(input_folder, output_csv)`

Merges all CSV files in the input folder into a single CSV file.

- **Parameters**:
  - `input_folder`: Path to the folder containing CSV files
  - `output_csv`: Path and filename for the output merged CSV

### `main()`

Main function that parses command-line arguments and calls the merge functions.

## Output

- A single MP4 file containing all merged video segments
- A single CSV file containing all merged tracking data, sorted by frame number

## Notes

- The script assumes that the last number in each filename represents the segment number for sorting purposes.
- Ensure you have sufficient disk space for the merged video file.
- Processing time may vary depending on the number and size of input files.

## Troubleshooting

- If you encounter a "file not found" error, check the paths to your input folder and ensure file naming conventions are correct.
- For "out of memory" errors when processing large videos, try increasing your system's swap space or processing the videos in smaller batches.

## Additional Information

- This script is designed to work in conjunction with output from video processing scripts that split videos into segments.
- Always backup your original files before running this merge operation.

For further assistance or to report issues, please contact the script author.
