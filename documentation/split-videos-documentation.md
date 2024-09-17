# split_videos.py Documentation

## Overview

`split_videos.py` is a Python script that splits a video file into multiple segments of a specified duration. It uses the MoviePy library to handle video processing.

## Requirements

- Python 3.x
- MoviePy library

You can install MoviePy using pip:

```
pip install moviepy
```

## Usage

Run the script from the command line with the following syntax:

```
python split_videos.py <video_path> <output_folder> [-d DURATION]
```

### Arguments:

- `video_path`: Path to the input video file (required)
- `output_folder`: Path to the folder where output segments will be saved (required)
- `-d DURATION`, `--duration DURATION`: Desired duration of each segment in seconds (optional, default: 1200 seconds / 20 minutes)

### Example:

To split a video into 20-minute segments:

```
python split_videos.py path/to/your/video.mp4 path/to/output/folder
```

To split a video into 10-minute segments:

```
python split_videos.py path/to/your/video.mp4 path/to/output/folder -d 600
```

## Functions

### `split_video(video_path, output_folder, segment_duration=20*60)`

This function is responsible for splitting the video into segments.

#### Parameters:

- `video_path` (str): Path to the input video file.
- `output_folder` (str): Path to the folder where output segments will be saved.
- `segment_duration` (int, optional): Desired duration of each segment in seconds. Default is 1200 seconds (20 minutes).

#### Behavior:

1. Opens the video file using MoviePy.
2. Calculates the total duration of the video.
3. Iteratively creates segments of the specified duration until the entire video is processed.
4. Saves each segment as a separate file in the output folder.
5. Closes the video file after processing.

### `main()`

This function handles the command-line interface of the script.

#### Behavior:

1. Sets up argument parsing using `argparse`.
2. Defines and parses the command-line arguments (video_path, output_folder, and duration).
3. Ensures the output folder exists, creating it if necessary.
4. Calls the `split_video()` function with the provided arguments.

## Output

The script will create multiple video files in the specified output folder. Each file will be named `segment_X.mp4`, where X is the segment number (starting from 1).

## Notes

- The script uses the MP4 format for output segments. If you need a different format, modify the `write_videofile()` call in the `split_video()` function.
- The last segment may be shorter than the specified duration if the video length is not evenly divisible by the segment duration.
- Ensure you have sufficient disk space in the output folder for all the video segments.
