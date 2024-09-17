# process_video_folder.py Documentation

## Overview

`process_video_folder.py` is a Python script that processes video segments using a YOLOv10 model for object detection and tracking. It takes a folder of video segments as input, processes each video, and outputs annotated videos along with CSV files containing tracking data.

## Requirements

- Python 3.x
- OpenCV (cv2)
- Ultralytics YOLOv10
- tqdm
- IPython

You can install the required packages using pip:

```
pip install opencv-python ultralytics tqdm ipython
```

## Usage

Run the script from the command line with the following syntax:

```
python process_video_folder.py <model_path> <segments_folder>
```

### Arguments:

- `model_path`: Path to the YOLOv10 model file (.pt)
- `segments_folder`: Path to the folder containing video segments to be processed

### Example:

```
python process_video_folder.py path/to/your/yolov10_model.pt path/to/your/segments/folder
```

## Functions

### `process_video_folder(model_path, segments_folder)`

This is the main function that processes all video segments in the specified folder.

#### Parameters:

- `model_path` (str): Path to the YOLOv10 model file.
- `segments_folder` (str): Path to the folder containing video segments.

#### Behavior:

1. Loads the YOLOv10 model.
2. Iterates through all .mp4 files in the specified folder.
3. For each video:
   - Opens the video file.
   - Creates an output video file with "_output" appended to the original filename.
   - Creates a CSV file for tracking data with "_output.csv" appended to the original filename.
   - Processes each frame of the video:
     - Applies YOLOv10 object detection and tracking.
     - Annotates the frame with detection results.
     - Writes the annotated frame to the output video.
     - Writes tracking data to the CSV file.
   - Displays progress using a tqdm progress bar.
4. Closes all open files and releases resources.

### `main()`

This function handles the command-line interface of the script.

#### Behavior:

1. Sets up argument parsing using `argparse`.
2. Defines and parses the command-line arguments (model_path and segments_folder).
3. Calls the `process_video_folder()` function with the provided arguments.

## Output

For each input video segment, the script produces:

1. An annotated video file: `original_filename_output.mp4`
2. A CSV file with tracking data: `original_filename_output.csv`

### CSV Format:

The CSV file contains the following columns:
- Frame: The frame number
- ID: Unique identifier for each tracked object
- Class: The class of the detected object
- X: X-coordinate of the object's center
- Y: Y-coordinate of the object's center

## Notes

- The script uses the MP4V codec for output videos. Ensure your system supports this codec, or modify the `fourcc` variable if needed.
- The script assumes that the YOLOv10 model file is compatible with the Ultralytics YOLOv10 implementation.
- Processing time may vary depending on the length and complexity of the videos, as well as the performance of your system and GPU.
- Ensure you have sufficient disk space for the output videos and CSV files.
- The script uses IPython's `clear_output()` function, which may not work in all environments. If you encounter issues, you can safely remove or comment out this line.

## Error Handling

The script does not include extensive error handling. Ensure that:
- The provided model file exists and is a valid YOLOv10 model.
- The segments folder exists and contains .mp4 files.
- You have write permissions in the segments folder for creating output files.

If you encounter any errors, check these conditions and ensure all required libraries are correctly installed.
