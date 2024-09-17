import csv
from collections import defaultdict
import numpy as np
import argparse

def process_csv(input_csv, output_csv, threshold=50.0):
    # Read the input CSV file
    with open(input_csv, 'r') as infile:
        reader = csv.DictReader(infile)
        data = list(reader)

    print(f"Total input rows: {len(data)}")

    # Group data by Frame, then by Class
    grouped_data = defaultdict(lambda: defaultdict(list))
    for row in data:
        frame = int(row['Frame'])
        class_id = int(row['Class'])
        grouped_data[frame][class_id].append((float(row['X']), float(row['Y'])))

    # Process data frame by frame
    processed_data = []
    duplicate_count = 0
    for frame, frame_data in sorted(grouped_data.items()):
        for mouse_index in range(5):  # Assuming 5 mice
            body_class = mouse_index * 2
            head_class = mouse_index * 2 + 1

            body_points = frame_data.get(body_class, [])
            head_points = frame_data.get(head_class, [])

            # Count duplicates
            duplicate_count += len(body_points) - 1 if body_points else 0
            duplicate_count += len(head_points) - 1 if head_points else 0

            # Handle body points
            if body_points:
                if len(body_points) > 1:
                    if head_points:
                        head_point = head_points[0]  # Use the first head point as reference
                        body_point = min(body_points, key=lambda p: ((p[0]-head_point[0])**2 + (p[1]-head_point[1])**2)**0.5)
                    else:
                        body_point = body_points[0]  # If no head point, use the first body point
                else:
                    body_point = body_points[0]

                processed_data.append({
                    'Frame': frame,
                    'ID': f'Class_{body_class}',
                    'Class': body_class,
                    'X': body_point[0],
                    'Y': body_point[1]
                })

            # Handle head points
            if head_points:
                if len(head_points) > 1:
                    if body_points:
                        body_point = body_points[0]  # Use the first body point as reference
                        head_point = min(head_points, key=lambda p: ((p[0]-body_point[0])**2 + (p[1]-body_point[1])**2)**0.5)
                    else:
                        head_point = head_points[0]  # If no body point, use the first head point
                else:
                    head_point = head_points[0]

                processed_data.append({
                    'Frame': frame,
                    'ID': f'Class_{head_class}',
                    'Class': head_class,
                    'X': head_point[0],
                    'Y': head_point[1]
                })

    print(f"Rows after initial processing: {len(processed_data)}")
    print(f"Duplicates removed: {duplicate_count}")

    # Sort processed data by Frame, then by Class
    processed_data.sort(key=lambda x: (x['Frame'], x['Class']))

    # Interpolate missing frames and apply threshold
    interpolated_data = interpolate_and_threshold(processed_data, threshold)

    print(f"Rows after interpolation and thresholding: {len(interpolated_data)}")

    # Write processed and interpolated data to CSV
    with open(output_csv, 'w', newline='') as outfile:
        fieldnames = ['Frame', 'ID', 'Class', 'X', 'Y']
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(interpolated_data)

    print(f"Output CSV rows: {len(interpolated_data)}")

def interpolate_and_threshold(data, threshold):
    # Group data by Class
    grouped_data = defaultdict(list)
    for row in data:
        grouped_data[row['Class']].append(row)

    interpolated_data = []

    for class_id, class_data in grouped_data.items():
        frames = np.array([row['Frame'] for row in class_data])
        x_values = np.array([float(row['X']) for row in class_data])
        y_values = np.array([float(row['Y']) for row in class_data])

        # Create a full range of frames
        full_frames = np.arange(frames.min(), frames.max() + 1)

        # Interpolate X and Y values
        x_interp = np.interp(full_frames, frames, x_values)
        y_interp = np.interp(full_frames, frames, y_values)

        # Apply threshold to interpolated values
        prev_x, prev_y = x_interp[0], y_interp[0]
        for i, (frame, x, y) in enumerate(zip(full_frames, x_interp, y_interp)):
            if i > 0:
                if abs(x - prev_x) > threshold or abs(y - prev_y) > threshold:
                    print(f"Class {class_id}, Frame {frame}: Threshold exceeded. Previous: ({prev_x}, {prev_y}), Current: ({x}, {y})")
                    x, y = prev_x, prev_y
            interpolated_data.append({
                'Frame': int(frame),
                'ID': f'Class_{class_id}',
                'Class': class_id,
                'X': x,
                'Y': y
            })
            prev_x, prev_y = x, y

    # Sort interpolated data by Frame, then by Class
    interpolated_data.sort(key=lambda x: (x['Frame'], x['Class']))
    return interpolated_data

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process CSV file for mouse tracking data.")
    parser.add_argument("input_csv", help="Path to the input CSV file")
    parser.add_argument("output_csv", help="Path to the output CSV file")
    parser.add_argument("-t", "--threshold", type=float, default=500.0,
                        help="Threshold for interpolation (default: 500.0)")
    args = parser.parse_args()

    process_csv(args.input_csv, args.output_csv, args.threshold)
