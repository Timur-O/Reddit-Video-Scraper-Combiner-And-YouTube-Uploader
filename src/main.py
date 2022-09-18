import reddit_scraper
import downloader
import editor


def main():
    print("Bot has started successfully!")
    print("Initializing scraper...")

    scraper = reddit_scraper.RedditScraper()
    # Scape the necessary posts
    scraper.scrape_posts()

    print("Beginning to Download Videos...")

    # Get the download URLs
    download_urls = scraper.get_download_urls()

    # Download the videos to the data folder
    downloader.download_all(download_urls)

    print("Beginning to Combine Videos...")

    # Combine the videos
    editor.combine_videos()


if __name__ == "__main__":
    main()
