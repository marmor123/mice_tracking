# Mouse Tracking Project

This repository contains a set of tools for processing and analyzing mouse tracking data from video footage. The project includes scripts for video processing, data analysis, and visualization using various Python libraries and Blender.

## Table of Contents

1. [Overview](#overview)
2. [Features](#features)
3. [Installation](#installation)
4. [Components](#components)
5. [Usage](#usage)
6. [Data Format](#data-format)
7. [Workflow](#workflow)
8. [Troubleshooting](#troubleshooting)
9. [Contributing](#contributing)
10. [Contact](#contact)

## Overview

This project aims to facilitate the analysis of mouse behavior by providing tools for:

- Splitting large video files into manageable segments
- Processing video segments to track mouse movements using YOLOv10
- Analyzing and visualizing tracking data
- Merging processed video segments and data
- Importing and manipulating tracking data in Blender

The tools are designed to work with data from multiple mice, tracking both body and head positions.

## Features

- Video splitting for efficient processing of large datasets
- YOLOv10-based object detection and tracking
- CSV data processing with interpolation and thresholding
- Merging of processed video segments and tracking data
- Blender add-on for advanced visualization and manipulation of tracking data
- Support for training custom YOLOv10 models

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/your-username/mouse-tracking-project.git
   cd mouse-tracking-project
   ```

2. Install the required Python libraries:
   ```
   pip install -r requirements.txt
   ```

3. Install additional dependencies:
   - CUDA and cuDNN (for GPU acceleration)
   - FFmpeg (for video processing)

4. For the Blender add-on:
   - Open Blender
   - Go to Edit > Preferences > Add-ons
   - Click "Install" and select the `tracking_blender.py` file
   - Enable the "Motion Tracking: Mouse Tracker Import/Export" add-on

## Components

- `split_videos.py`: Splits large video files into smaller segments
- `process_video_folder.py`: Processes video segments using YOLOv10 for object detection and tracking
- `csv-processor-cli.py`: Processes CSV files containing mouse tracking data
- `merge-videos-and-csv.py`: Merges processed video segments and CSV files
- `tracking_blender.py`: Blender add-on for importing, visualizing, and manipulating tracking data
- `train-yolov10.ipynb`: Jupyter notebook for training the YOLOv10 model on custom data

## Usage

### Splitting Videos

```
python split_videos.py <video_path> <output_folder> [-d DURATION]
```
Example:
```
python split_videos.py long_video.mp4 ./segments -d 600
```

### Processing Video Segments

```
python process_video_folder.py <model_path> <segments_folder>
```
Example:
```
python process_video_folder.py ./models/yolov10m.pt ./segments
```

### Processing CSV Data

```
python csv-processor-cli.py <input_csv> <output_csv> [-t THRESHOLD]
```
Example:
```
python csv-processor-cli.py raw_data.csv processed_data.csv -t 50.0
```

### Merging Processed Videos and CSV Files

```
python merge-videos-and-csv.py <input_folder> <output_video> <output_csv>
```
Example:
```
python merge-videos-and-csv.py ./processed_segments merged_video.mp4 merged_data.csv
```

### Blender Add-on

1. In Blender, go to the Movie Clip Editor
2. Open the "Mouse Tracker I/O" panel in the sidebar (press N if not visible)
3. Use the panel to import, export, and process tracking data

### Training YOLOv10

1. Open the `train-yolov10.ipynb` notebook in Jupyter
2. Follow the instructions to prepare your dataset and train the model
3. Adjust hyperparameters as needed for your specific use case

## Data Format

The CSV files used in this project have the following columns:
- Frame: The frame number
- ID: Unique identifier for each tracked object (e.g., "Class_0", "Class_1")
- Class: Numeric class identifier (even numbers for body, odd for head)
- X: X-coordinate of the tracked point
- Y: Y-coordinate of the tracked point

## Workflow

1. Split large videos into segments using `split_videos.py`
2. Process video segments with `process_video_folder.py`
3. (Optional) Further process the CSV data with `csv-processor-cli.py`
4. Merge processed segments using `merge-videos-and-csv.py`
5. Import the merged data into Blender for visualization and analysis

## Troubleshooting

- **CUDA errors**: Ensure you have the correct CUDA and cuDNN versions installed for your GPU and PyTorch version.
- **Video processing issues**: Check that FFmpeg is properly installed and accessible in your system PATH.
- **CSV processing errors**: Verify that your input CSV files match the expected format described in the [Data Format](#data-format) section.
- **Blender add-on not working**: Make sure you've enabled the add-on in Blender preferences and that it's compatible with your Blender version.

If you encounter persistent issues, please check the [Issues](https://github.com/marmor123/mice_tracking/issues) section of the repository or open a new issue with a detailed description of the problem.

