import reddit_scraper
import downloader
import editor
from src import uploader


def main():
    print("Bot has started successfully!")
    print("Initializing scraper...")

    scraper = reddit_scraper.RedditScraper()
    # Scape the necessary posts
    scraper.scrape_posts()

    print("Beginning to Download Videos...")

    # Get the download URLs
    download_urls = scraper.get_download_urls()
    video_credits = scraper.get_credits()
    thumbnails = scraper.get_thumbnails()

    # Download the videos to the data folder
    downloader.download_all(download_urls)

    print("Beginning to Create Thumbnail")

    downloader.download_thumbnail(thumbnails)

    print("Beginning to Combine Videos...")

    # Combine the videos
    editor.combine_videos()

    print("Beginning to Upload the Video...")

    # Upload the videos
    uploader.upload(video_credits)

    print("Bot has completed successfully!")


if __name__ == "__main__":
    main()
