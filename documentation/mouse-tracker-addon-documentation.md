# Mouse Tracker Import/Export Add-on Documentation

## Overview

The Mouse Tracker Import/Export add-on for Blender is designed to facilitate the import, export, and processing of mouse tracking data in the Blender Movie Clip Editor. This add-on is particularly useful for researchers and animators working with mouse behavior analysis or similar tracking data.

## Installation

1. Download the `tracking_blender.py` file.
2. Open Blender and go to Edit > Preferences > Add-ons.
3. Click "Install" and navigate to the downloaded `tracking_blender.py` file.
4. Enable the add-on by checking the box next to "Motion Tracking: Mouse Tracker Import/Export".

## Features

- Import and process CSV tracking data
- Load associated video into the Movie Clip Editor
- Export processed tracking data
- Reprocess individual tracks from a specific frame

## Usage

After installation, you can access the add-on in the Movie Clip Editor under the "Mouse Tracker I/O" tab in the sidebar (press N if the sidebar is not visible).

### Importing and Processing Data

1. In the "Import and Process" section:
   - Set the "Input CSV" path to your raw tracking data CSV file.
   - Set the "Input MP4" path to your video file.
   - Set the "Processed CSV" path where you want to save the processed data. This step is crucial and must be done before importing.
   - Adjust the "Movement Threshold" if needed (default is 50.0).
   - Click "Import and Process Trackers".

This action will:
- Process the input CSV file, applying the movement threshold.
- Save the processed data to the specified "Processed CSV" path.
- Load the video into the Movie Clip Editor.
- Create tracking markers based on the processed data.

### Exporting Data

1. In the "Export" section:
   - Ensure the "Processed CSV" path is set to where you want to save the exported data. This should typically be the same location you specified during the import process.
   - Click "Export Trackers".

This will export the current state of all trackers in the Movie Clip Editor to the specified CSV file.

### Reprocessing a Track

1. In the "Reprocess Track" section:
   - Select the tracker you want to reprocess from the dropdown menu.
   - Ensure you're on the frame from which you want to start reprocessing.
   - Click "Reprocess Track".

This will:
- Reprocess the selected track from the current frame to the end of the video.
- Update the track in the Movie Clip Editor with the reprocessed data.
- Save the updated data to the "Processed CSV" file specified in the import/export sections.

## CSV File Format

The add-on expects and produces CSV files with the following columns:
- Frame: The frame number
- ID: Unique identifier for each tracked object (e.g., "Class_0", "Class_1")
- Class: Numeric class identifier
- X: X-coordinate of the tracked point
- Y: Y-coordinate of the tracked point

## Notes

- The add-on assumes that classes are paired (e.g., class 0 and 1 represent body and head of the same mouse).
- The movement threshold is applied to prevent unrealistic jumps in tracker positions.
- When reprocessing, the threshold is not applied for the first second (based on video FPS) to allow for initial adjustments.
- Always ensure that the "Processed CSV" path is set correctly before performing any import, export, or reprocessing operations.

## Troubleshooting

- If no data is exported, check if there are any valid trackers in the Movie Clip Editor.
- Ensure that your input CSV and video files are in the correct format and accessible.
- If trackers appear in incorrect positions, check if the video dimensions match those used in the original tracking process.
- If you encounter issues with importing or exporting, verify that the "Processed CSV" path is correctly set and that you have write permissions for that location.

## Additional Information

- The add-on uses the Blender Python API and libraries such as OpenCV and NumPy.
- For large datasets, processing might take some time. Be patient during import and export operations.
- Always backup your original data before processing or reprocessing.

For further assistance or to report issues, please contact the add-on author, Dvir Marmor.
