import configparser
import numpy as np

from pathlib import Path
from moviepy.editor import *


def combine_videos():
    configFilePath = "config.txt"
    parser = configparser.ConfigParser()
    parser.read_file(open(configFilePath, "r"))

    data_folder_path = Path(__file__) / parser.get('Output Config', 'data_path')

    # Define variables and helper functions
    videos = []
    cut = lambda i: temp_clip.audio.subclip(i, i + 1).to_soundarray(fps=22000)
    volume = lambda array: np.sqrt(((1.0 * array) ** 2).mean())

    # Get all the videos in the data directory
    for file in os.listdir(str(data_folder_path)):
        # Skip reused data
        if file.endswith("data-reuse") or not file.endswith(".mp4"):
            continue

        temp_clip = VideoFileClip(str(data_folder_path / file)).resize(height=1080)

        volumes = [volume(cut(i)) for i in range(0, int(temp_clip.audio.duration))]
        max_volume = np.max(volumes)

        # Skip videos without audio
        if np.isclose(max_volume, 0.0):
            print("Skipping Muted...")
            continue

        videos.append(temp_clip)

    # Concatenate ending clip to video
    if parser.get('Content Config', 'append_clip').lower() in ['true', 'yes', 'y', '1']:
        videos.append(VideoFileClip(str(data_folder_path / parser.get('Content Config',
                                                                      'append_clip_location_relative_to_data_path')))
                      .resize(height=1080))

    # Concatenate the video
    final_video = concatenate_videoclips(videos, method="compose")

    # Get the output file name
    output_filename = parser.get('Output Config', 'output_filename')

    # Save the concatenated video
    final_video.write_videofile(str(data_folder_path / output_filename))

    print("Combined Successfully!")
