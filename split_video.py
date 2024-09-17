import moviepy.editor as mp
import argparse
import os

def split_video(video_path, output_folder, segment_duration=20*60):
    """
    Splits a video into segments of approximately `segment_duration` seconds
    and saves them in the specified `output_folder`.

    Args:
        video_path (str): Path to the input video file.
        output_folder (str): Path to the folder where output segments will be saved.
        segment_duration (int): Desired duration of each segment in seconds (default: 20 minutes).
    """

    video = mp.VideoFileClip(video_path)
    total_duration = video.duration
    start_time = 0

    segment_count = 1
    while start_time < total_duration:
        end_time = min(start_time + segment_duration, total_duration)
        segment = video.subclip(start_time, end_time)
        segment.write_videofile(f"{output_folder}/segment_{segment_count}.mp4")  # Adjust output format if needed
        start_time += segment_duration
        segment_count += 1

    video.close()

def main():
    parser = argparse.ArgumentParser(description="Split a video into segments.")
    parser.add_argument("video_path", help="Path to the input video file")
    parser.add_argument("output_folder", help="Path to the folder where output segments will be saved")
    parser.add_argument("-d", "--duration", type=int, default=1200,
                        help="Desired duration of each segment in seconds (default: 1200 seconds / 20 minutes)")

    args = parser.parse_args()

    # Ensure the output folder exists
    os.makedirs(args.output_folder, exist_ok=True)

    split_video(args.video_path, args.output_folder, args.duration)

if __name__ == "__main__":
    main()
