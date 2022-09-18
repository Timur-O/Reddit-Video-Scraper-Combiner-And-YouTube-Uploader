import configparser
import numpy as np

from pathlib import Path
from moviepy.editor import *


def combine_videos():
    configFilePath = "../config.txt"
    parser = configparser.ConfigParser()
    parser.read_file(open(configFilePath, "r"))

    if parser.get('Output Config', 'data_path') != '':
        data_folder_path = Path(parser.get('Output Config', 'data_path'))
    else:
        data_folder_path = Path(__file__).parent.parent / "data"

    # Define variables and helper functions
    videos = []
    cut = lambda i: temp_clip.audio.subclip(i, i + 1).to_soundarray(fps=22000)
    volume = lambda array: np.sqrt(((1.0 * array) ** 2).mean())

    # Get all the videos in the data directory
    for file in os.listdir(str(data_folder_path)):
        temp_clip = VideoFileClip(str(data_folder_path / file)).resize(height=1080)

        volumes = [volume(cut(i)) for i in range(0, int(temp_clip.audio.duration))]
        max_volume = np.max(volumes)

        # Skip videos without audio
        if (np.isclose(max_volume, 0.0)):
            print("Skipping Muted...")
            continue

        videos.append(temp_clip)

    # Concatenate the video
    final_video = concatenate_videoclips(videos, method="compose")

    # Get the output file name
    output_filename = parser.get('Output Config', 'output_filename')

    # Save the concatenated video
    final_video.write_videofile(str(data_folder_path / output_filename))

    # Delete unnecessary separate videos
    if parser.get('Output Config', 'delete_separate_clips').lower() in ['true', 'yes', 'y', '1']:
        for video in os.listdir(str(data_folder_path)):
            if not video.endswith(output_filename):
                os.remove(video)

    print("Combined Successfully!")
