import praw
import configparser


class RedditScraper:
    def __init__(self):
        """
            Initializes the reddit object.
        """
        # Setup Config
        configFilePath = "../config.txt"
        self.parser = configparser.ConfigParser()
        self.parser.read_file(open(configFilePath, "r"))

        # Get Reddit Config Info
        client_id = self.parser.get('Reddit Scraper Config', 'client_id')
        client_secret = self.parser.get('Reddit Scraper Config', 'client_secret')
        user_agent = self.parser.get('Reddit Scraper Config', 'user_agent')
        username = self.parser.get('Reddit Scraper Config', 'reddit_username')
        password = self.parser.get('Reddit Scraper Config', 'reddit_password')

        # Initialize Reddit Object
        self.reddit = praw.Reddit(
            client_id=client_id,
            client_secret=client_secret,
            password=password,
            user_agent=user_agent,
            username=username
        )

        # Initialize Other Variables
        self.video_urls = []

        # Inform user of status
        print("Initialized Successfully!")

    def scrape_posts(self):
        """
        Scrapes the posts from the subreddit and adds them to the list of posts
        """
        # Inform user of status
        print("Beginning to Scrape...")

        # Get Content Config Info
        subreddits: str = self.parser.get('Content Config', 'list_of_subreddits')\
                                     .replace('[', '')\
                                     .replace(',', '+')\
                                     .replace(']', '')
        top_time_limit: str = self.parser.get('Content Config', 'top_time_limit')
        max_submission_length: int = int(self.parser.get('Content Config', 'max_submission_duration_seconds'))
        allow_nsfw: bool = self.parser.get('Content Config', 'allow_nsfw').lower() in ['true', 'yes', 'y', '1']
        allow_previous: bool = self.parser.get('Content Config', 'allow_previous').lower() in ['true', 'yes', 'y', '1']
        final_video_duration_max: int = int(self.parser.get('Content Config', 'final_video_soft_max_duration'))

        # Begin Scraping
        # Create fetching iterator, only fetches on iterating through an element
        curr_batch = self.reddit.subreddit(subreddits).top(time_filter=top_time_limit, limit=None)
        curr_duration = 0

        for submission in curr_batch:
            # Filter out NSFW content from current batch if set
            if not allow_nsfw and submission.over_18:
                print("Skipping NSFW...")
                continue

            # Filter out previously used content from current batch if set
            if not allow_previous and submission.saved:
                print("Skipping Saved...")
                continue

            # The try-except ensures that only reddit hosted videos are included, not ones on other platforms
            try:
                submission_duration = int(submission.secure_media['reddit_video']['duration'])
            except Exception:
                print("Skipping Non-Video / Non-Reddit Video...")
                continue

            # Filter out too long videos
            if submission_duration > max_submission_length:
                print("Skipping Long...")
                continue

            # Video Matched Criteria => Add to list
            curr_duration += submission_duration
            self.video_urls.append(submission.url)

            # Save post to mark as "previous"
            if not submission.saved:
                submission.save()

            # Break loop once there are enough videos
            if curr_duration >= final_video_duration_max:
                break

        # Inform user of status
        print("Scraped Successfully!")

    def get_download_urls(self):
        """
        Returns the URLs of the posts to be downloaded
        Returns:
        -----
        self.video_urls: list, a list of the post URLs to download
        """
        return self.video_urls
