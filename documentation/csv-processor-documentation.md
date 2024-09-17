# CSV Processor for Mouse Tracking Data

## Overview

This Python script, `csv-processor-cli.py`, processes CSV files containing mouse tracking data. It performs the following main tasks:

1. Reads input CSV data
2. Processes and consolidates multiple data points for each mouse
3. Interpolates missing frames
4. Applies a threshold to limit sudden movements
5. Outputs the processed data to a new CSV file

The script is designed to handle data for 5 mice, each represented by two classes (body and head).

## Installation

Ensure you have Python 3.x installed on your system. This script requires the following Python libraries:

- csv (built-in)
- collections (built-in)
- numpy
- argparse (built-in)

You can install numpy using pip:

```
pip install numpy
```

## Usage

Run the script from the command line with the following syntax:

```
python csv-processor-cli.py input_file.csv output_file.csv [-t THRESHOLD]
```

### Arguments:

- `input_file.csv`: Path to the input CSV file (required)
- `output_file.csv`: Path to the output CSV file (required)
- `-t THRESHOLD`, `--threshold THRESHOLD`: Threshold for interpolation (optional, default: 500.0)

### Examples:

1. Basic usage:
   ```
   python csv-processor-cli.py input_data.csv output_data.csv
   ```

2. With a custom threshold:
   ```
   python csv-processor-cli.py input_data.csv output_data.csv -t 300.0
   ```

3. To see the help message:
   ```
   python csv-processor-cli.py -h
   ```

## Input CSV Format

The input CSV file should have the following columns:

- Frame: The frame number
- Class: The class ID (0-9 for 5 mice, even numbers for body, odd for head)
- X: X-coordinate of the data point
- Y: Y-coordinate of the data point

## Output CSV Format

The output CSV file will have the following columns:

- Frame: The frame number
- ID: The class identifier (e.g., "Class_0", "Class_1")
- Class: The class ID (0-9)
- X: X-coordinate of the processed data point
- Y: Y-coordinate of the processed data point

## Detailed Function Descriptions

### `process_csv(input_csv, output_csv, threshold=50.0)`

This is the main function that orchestrates the entire process.

Parameters:
- `input_csv` (str): Path to the input CSV file
- `output_csv` (str): Path to the output CSV file
- `threshold` (float, optional): Threshold for interpolation. Default is 50.0

Steps:
1. Reads the input CSV file
2. Groups data by Frame and Class
3. Processes data frame by frame, handling multiple points for body and head
4. Sorts processed data
5. Calls `interpolate_and_threshold` to interpolate missing frames and apply the threshold
6. Writes the processed and interpolated data to the output CSV file

### `interpolate_and_threshold(data, threshold)`

This function interpolates missing frames and applies a threshold to limit sudden movements.

Parameters:
- `data` (list): List of dictionaries containing processed data
- `threshold` (float): Maximum allowed movement between consecutive frames

Steps:
1. Groups data by Class
2. For each class:
   - Interpolates X and Y values for missing frames
   - Applies the threshold, replacing values that exceed it with the previous valid value
3. Sorts the interpolated data

Returns:
- List of dictionaries containing the interpolated and thresholded data

## Notes

- The script assumes data for 5 mice, each with a body (even class numbers) and head (odd class numbers) point.
- When multiple points are found for a single class in a frame, the script chooses the point closest to the corresponding head/body point.
- The interpolation process fills in missing frames with estimated values.
- The thresholding process prevents unrealistic sudden movements by capping the distance a point can move between consecutive frames.

## Troubleshooting

If you encounter any issues:
- Ensure your input CSV file is correctly formatted
- Check that you have all required libraries installed
- Verify that you're using the correct command-line syntax
- Try adjusting the threshold value if the output seems incorrect

For any persistent problems, please contact the script maintainer.
