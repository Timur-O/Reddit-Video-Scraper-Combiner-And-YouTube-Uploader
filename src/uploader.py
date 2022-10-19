"""
This file contains everything pertaining to uploading the content to YouTube.
"""
import os
from pathlib import Path

from simple_youtube_api.channel import Channel
from simple_youtube_api.local_video import LocalVideo

from src.title_generator import TitleGenerator


class YouTubeUploader:
    """
    This class contains all the data and methods for uploading to YouTube.
    """
    def __init__(self, parser, video_credits: list):
        # Setup Config
        self.parser = parser
        self.data_folder_path = Path(__file__) / self.parser.get('Output Config', 'data_path')
        self.output_filename = self.parser.get('Output Config', 'output_filename')

        client_secret_location = self.data_folder_path / self.parser.get('YouTube Config', 'client_secret_location')
        credentials_storage_location = self.data_folder_path / self.parser.get('YouTube Config', 'login_storage_path')
        scope_urls = self.parser.get('YouTube Config', 'scope_urls').split(',')
        show_login_button = self.parser.get('YouTube Config', 'show_login_button').lower() in ['true', 'yes', 'y', '1']
        login_button_url = self.parser.get('YouTube Config', 'login_button_location')

        self.channel = Channel(show_login_button, self.data_folder_path / login_button_url)
        self.channel.login(str(client_secret_location),
                           str(credentials_storage_location),
                           scope_urls)

        # Select the Video
        self.video = LocalVideo(file_path=str(self.data_folder_path / self.output_filename))

        # Generate and set a title
        title_generator = TitleGenerator(parser)
        title = title_generator.generate()
        self.video.set_title(title)

        # Append credits to description and set description
        with open(self.data_folder_path / self.parser.get('YouTube Metadata Config', 'description_location'),
                  encoding="utf8") as file:
            description = file.read()
            for credit in video_credits:
                description += "\n- " + credit
        self.video.set_description(description)

        # Set the tags
        with open(self.data_folder_path / self.parser.get('YouTube Metadata Config', 'tags_location'),
                  encoding="utf8") as file:
            lines = file.readlines()
            tags = [line.rstrip() for line in lines]
        self.video.set_tags(tags)

        # Set embeddability, public stats, and privacy status
        self.video.set_embeddable(True)
        self.video.set_public_stats_viewable(True)
        self.video.set_privacy_status(self.parser.get('YouTube Metadata Config', 'privacy'))

        # These are set by default on the YouTube Channel
        # self.video.set_category("comedy")
        # self.video.set_license("youtube")
        # self.video.set_made_for_kids(False)
        # self.video.set_default_language("en-US")

        # Set Thumbnail
        self.video.set_thumbnail_path(str(self.data_folder_path / self.parser.get('Output Config', 'output_thumbnail')))

    def upload(self):
        """
        Uploads the video to YouTube
        Returns:
        -----
        youtube_video.id: str, the id of the uploaded YouTube video
        """
        youtube_video = self.channel.upload_video(self.video)
        return youtube_video.id

    def clean_up(self):
        """
        Cleans up the downloaded clips and thumbnails
        """
        print("Deleting Clips...")

        # Delete unnecessary separate videos if set
        if self.parser.get('Output Config', 'delete_separate_clips').lower() in ['true', 'yes', 'y', '1']:
            for video in os.listdir(str(self.data_folder_path)):
                if not video.endswith(self.output_filename) and not video.endswith("data-reuse"):
                    os.remove(str(self.data_folder_path / video))

        # Delete combined clip if set
        if self.parser.get('Output Config', 'delete_combined_video').lower() in ['true', 'yes', 'y', '1']:
            os.remove(str(self.data_folder_path / self.output_filename))

        print("Deleted Successfully!")
