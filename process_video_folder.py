import cv2
from ultralytics import YOLOv10
from tqdm import tqdm
import csv
from IPython.display import clear_output
import os
import argparse

def process_video_folder(model_path, segments_folder):
    # Load the YOLOv10 model
    model = YOLOv10(model_path)

    # Get a list of all video files in the segments folder
    video_files = [f for f in os.listdir(segments_folder) if f.endswith('.mp4')]

    # Loop through each video segment
    for video_file in video_files:
        # Construct the full path to the video segment
        video_path = os.path.join(segments_folder, video_file)

        # Open the video file
        cap = cv2.VideoCapture(video_path)

        # Get video properties
        frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = int(cap.get(cv2.CAP_PROP_FPS))

        # Define the codec and create VideoWriter object, using the original video filename with "_output" appended
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        output_video_path = os.path.join(segments_folder, f"{os.path.splitext(video_file)[0]}_output.mp4")
        out = cv2.VideoWriter(output_video_path, fourcc, fps, (frame_width, frame_height))

        # Prepare CSV file, using the original video filename with "_output.csv" appended
        csv_path = os.path.join(segments_folder, f"{os.path.splitext(video_file)[0]}_output.csv")
        csv_file = open(csv_path, 'w', newline='')
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(['Frame', 'ID', 'Class', 'X', 'Y'])

        frame_count = 0
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

        # Loop through the video frames with progress bar
        with tqdm(total=total_frames, desc=f"Processing {video_file}", unit="frame") as pbar:
            while cap.isOpened():
                # Read a frame from the video
                success, frame = cap.read()
                if success:
                    # Run YOLOv10 tracking on the frame, persisting tracks between frames
                    results = model.track(frame, persist=True)

                    # Visualize the results on the frame
                    annotated_frame = results[0].plot()

                    # Write the frame to the output video
                    out.write(annotated_frame)

                    # Write tracking information to CSV
                    if results[0].boxes.id is not None:
                        boxes = results[0].boxes.xywh.cpu().numpy()
                        track_ids = results[0].boxes.id.cpu().numpy().astype(int)
                        classes = results[0].boxes.cls.cpu().numpy().astype(int)

                        for box, track_id, cls in zip(boxes, track_ids, classes):
                            x, y, w, h = box
                            csv_writer.writerow([frame_count, track_id, cls, x, y])

                    frame_count += 1
                    pbar.update(1)  # Update the progress bar

                    # Print processing time information (optional), clearing previous output
                    if results[0].boxes.id is not None:
                        clear_output(wait=True)  # Clear previous output
                        print(f"Frame {frame_count}/{total_frames}")

                else:
                    # Break the loop if the end of the video is reached
                    break

        # Release the video capture and writer objects
        cap.release()
        out.release()
        csv_file.close()

        print(f"Video processing completed for {video_file}. Output saved.")
        print(f"Tracking data saved as '{csv_path}'.")

def main():
    parser = argparse.ArgumentParser(description="Process video segments using YOLOv10 model.")
    parser.add_argument("model_path", help="Path to the YOLOv10 model file")
    parser.add_argument("segments_folder", help="Path to the folder containing video segments")

    args = parser.parse_args()

    process_video_folder(args.model_path, args.segments_folder)

if __name__ == "__main__":
    main()
