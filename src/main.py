import src.reddit_scraper as reddit_scraper
import src.downloader as downloader
import src.editor as editor
import src.uploader as uploader


def main():
    print("Meme Machine has started successfully!")
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

    print("Beginning to Combine/Modify/Curate Videos...")

    # Combine the videos
    editor.combine_videos()

    print("Beginning to Upload the Video...")

    # Upload the videos
    uploader.upload(video_credits)

    print("Meme Machine has completed successfully!")


if __name__ == "__main__":
    main()
