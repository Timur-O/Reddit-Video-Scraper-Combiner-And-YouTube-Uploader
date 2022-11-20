"""
This file combines all the parts of the code and runs them to form the application.
"""
import configparser
from pathlib import Path

from src import downloader
from src import editor
from src import reddit_scraper
from src import uploader


def main():
    """
    The main function, which calls all the other necessary functions for the application.
    :return:
    """
    print("Meme Machine has started successfully!")

    config_file_path = "config.txt"
    parser = configparser.ConfigParser()
    with open(config_file_path, "r", encoding="utf8") as file:
        parser.read_file(file)

    data_folder_path = Path.cwd() / parser.get('Output Config', 'data_path')

    print("Initializing scraper...")

    mm_scraper = reddit_scraper.RedditScraper(parser, data_folder_path)
    # Scape the necessary posts
    mm_scraper.scrape_posts()

    print("Beginning to Download Videos...")

    # Get the download URLs
    download_urls = mm_scraper.get_download_urls()
    video_credits = mm_scraper.get_credits()
    thumbnails = mm_scraper.get_thumbnails()

    # Download the videos to the data folder
    mm_downloader = downloader.ContentDownloader(parser, data_folder_path)
    mm_downloader.download_all(download_urls)

    print("Beginning to Create Thumbnail")

    mm_downloader.download_thumbnail(thumbnails)

    print("Beginning to Combine/Modify/Curate Videos...")

    # Combine the videos
    mm_editor = editor.Editor(parser, data_folder_path)
    mm_editor.combine_videos()

    print("Beginning to Upload the Video...")

    # Upload the videos
    mm_uploader = uploader.YouTubeUploader(parser, data_folder_path, video_credits)
    mm_uploader.upload()

    # Clean up after uploading
    mm_uploader.clean_up()

    print("Meme Machine has completed successfully!")


if __name__ == "__main__":
    main()
