import os
from pathlib import Path

from simple_youtube_api.Channel import Channel
from simple_youtube_api.LocalVideo import LocalVideo

from src.title_generator import TitleGenerator


class YouTubeUploader:
    def __init__(self, parser, video_credits: list):
        # Setup Config
        self.parser = parser

        self.data_folder_path = Path(__file__) / self.parser.get('Output Config', 'data_path')
        self.output_filename = self.parser.get('Output Config', 'output_filename')

        client_secret_location = self.data_folder_path / self.parser.get('YouTube Config', 'client_secret_location')
        credentials_storage_location = self.data_folder_path / self.parser.get('YouTube Config', 'login_storage_path')
        scope_urls = self.parser.get('YouTube Config', 'scope_urls').split(',')

        self.channel = Channel()
        self.channel.login(str(client_secret_location),
                           str(credentials_storage_location),
                           scope_urls)

        # Select the Video
        self.video = LocalVideo(file_path=str(self.data_folder_path / self.output_filename))

        # Generate and set a title
        title_generator = TitleGenerator()
        self.title = title_generator.generate()
        self.video.set_title(self.title)

        # Append credits to description and set description
        with open(self.data_folder_path / self.parser.get('YouTube Metadata Config', 'description_location')) as file:
            self.description = file.read()
            for credit in video_credits:
                self.description += "\n- " + credit
        self.video.set_description(self.description)

        # Set the tags
        with open(self.data_folder_path / self.parser.get('YouTube Metadata Config', 'tags_location')) as file:
            lines = file.readlines()
            self.tags = [line.rstrip() for line in lines]
        self.video.set_tags(self.tags)

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
