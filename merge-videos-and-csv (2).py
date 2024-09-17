import os
import csv
import argparse
from moviepy.editor import VideoFileClip, concatenate_videoclips
import re

def sort_files(files):
    """Sort files based on the numeric part of their names."""
    def extract_number(filename):
        # Extract all numbers from the filename
        numbers = re.findall(r'\d+', filename)
        # Return the last number (assuming it's the segment number)
        return int(numbers[-1]) if numbers else 0

    return sorted(files, key=extract_number)

def merge_videos(input_folder, output_video):
    """Merge video segments into a single video file."""
    video_files = [f for f in os.listdir(input_folder) if f.endswith('_output.mp4')]
    video_files = sort_files(video_files)
    
    clips = [VideoFileClip(os.path.join(input_folder, f)) for f in video_files]
    final_clip = concatenate_videoclips(clips)
    final_clip.write_videofile(output_video)

def merge_csv_files(input_folder, output_csv):
    """Merge CSV files into a single CSV file with continuous frame numbers."""
    csv_files = [f for f in os.listdir(input_folder) if f.endswith('_output.csv')]
    csv_files = sort_files(csv_files)
    
    all_data = []
    last_frame = -1  # Initialize last_frame to -1
    
    for csv_file in csv_files:
        with open(os.path.join(input_folder, csv_file), 'r') as f:
            reader = csv.DictReader(f)
            segment_data = list(reader)
            
            # Adjust frame numbers for this segment
            for row in segment_data:
                new_frame = int(row['Frame']) + last_frame + 1
                row['Frame'] = str(new_frame)
            
            all_data.extend(segment_data)
            
            # Update last_frame for the next segment
            if segment_data:
                last_frame = int(segment_data[-1]['Frame'])
    
    # Sort all data by frame number (should already be in order, but just to be safe)
    all_data.sort(key=lambda x: int(x['Frame']))
    
    # Write sorted data to output CSV
    if all_data:
        keys = all_data[0].keys()
        with open(output_csv, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=keys)
            writer.writeheader()
            writer.writerows(all_data)

def main():
    parser = argparse.ArgumentParser(description="Merge processed video segments and CSV files.")
    parser.add_argument("input_folder", help="Path to the folder containing processed video segments and CSV files")
    parser.add_argument("output_video", help="Path for the output merged video file")
    parser.add_argument("output_csv", help="Path for the output merged CSV file")
    
    args = parser.parse_args()
    
    merge_videos(args.input_folder, args.output_video)
    merge_csv_files(args.input_folder, args.output_csv)
    
    print(f"Merged video saved to: {args.output_video}")
    print(f"Merged CSV saved to: {args.output_csv}")

if __name__ == "__main__":
    main()
