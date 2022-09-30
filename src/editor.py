"""
This files manages the editing of the content into one clip.
"""
import os
from pathlib import Path

import numpy as np
from moviepy.editor import VideoFileClip, concatenate_videoclips


class Editor:
    """
    This class edits the content.
    """

    def __init__(self, parser):
        """
            Initializes the editor object.
            Params:
            -----
            parser: Config Parser Instance
        """
        self.parser = parser

    def combine_videos(self):
        """
        Combines all the videos in the data folder that end in .mp4
        """
        data_folder_path = Path(__file__) / self.parser.get('Output Config', 'data_path')

        # Define variables and helper functions
        videos = []

        def cut_audio_clip(i: int):
            """
            Gets a one-second clip from audio channel of temp_clip, and converts to a sound array.
            Params:
            -----
            i: int, the second at which to clip the audio
            Returns:
            -----
            array: np.ndarray, the sound array of the one-second audio
            """
            return temp_clip.audio.subclip(i, i + 1).to_soundarray(fps=22000)

        def volume(array: np.ndarray):
            """
            Gets the average volume of the sound array.
            Params:
            ----
            array: np.ndarray, the sound array.
            Returns:
            -----
            volume: int, the average volume of the sound array
            """
            return np.sqrt(((1.0 * array) ** 2).mean())

        # Get all the videos in the data directory
        for file in os.listdir(str(data_folder_path)):
            # Skip reused data
            if file.endswith("data-reuse") or not file.endswith(".mp4"):
                continue

            temp_clip = VideoFileClip(str(data_folder_path / file)).resize(height=1080)

            volumes = [volume(cut_audio_clip(i)) for i in range(0, int(temp_clip.audio.duration))]
            max_volume = np.max(volumes)

            # Skip videos without audio
            if np.isclose(max_volume, 0.0):
                print("Skipping Muted...")
                continue

            videos.append(temp_clip)

        # Concatenate ending clip to video
        if self.parser.get('Content Config', 'append_clip').lower() in ['true', 'yes', 'y', '1']:
            videos.append(
                VideoFileClip(str(data_folder_path / self.parser.get('Content Config',
                                                                     'append_clip_location_relative_to_data_path')
                                  )).resize(height=1080)
            )

        # Concatenate the video
        final_video = concatenate_videoclips(videos, method="compose")

        # Get the output file name
        output_filename = self.parser.get('Output Config', 'output_filename')

        # Save the concatenated video
        final_video.write_videofile(str(data_folder_path / output_filename))

        print("Combined Successfully!")
