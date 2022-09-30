import src.reddit_scraper as reddit_scraper
import src.downloader as downloader
import src.editor as editor
import src.uploader as uploader
import configparser


def main():
    print("Meme Machine has started successfully!")

    configFilePath = "config.txt"
    parser = configparser.ConfigParser()
    parser.read_file(open(configFilePath, "r"))

    print("Initializing scraper...")

    mm_scraper = reddit_scraper.RedditScraper(parser)
    # Scape the necessary posts
    mm_scraper.scrape_posts()

    print("Beginning to Download Videos...")

    # Get the download URLs
    download_urls = mm_scraper.get_download_urls()
    video_credits = mm_scraper.get_credits()
    thumbnails = mm_scraper.get_thumbnails()

    # Download the videos to the data folder
    mm_downloader = downloader.ContentDownloader(parser)
    mm_downloader.download_all(download_urls)

    print("Beginning to Create Thumbnail")

    mm_downloader.download_thumbnail(thumbnails)

    print("Beginning to Combine/Modify/Curate Videos...")

    # Combine the videos
    mm_editor = editor.Editor(parser)
    mm_editor.combine_videos()

    print("Beginning to Upload the Video...")

    # Upload the videos
    mm_uploader = uploader.YouTubeUploader(parser, video_credits)
    mm_uploader.upload()

    # Clean up after uploading
    mm_uploader.clean_up()

    print("Meme Machine has completed successfully!")


if __name__ == "__main__":
    main()
