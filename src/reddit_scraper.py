"""
This file manages the scraping of content from Reddit.
"""
from datetime import datetime
from pathlib import Path

import praw


class RedditScraper:
    """
    This class scrapes content from Reddit.
    """
    def __init__(self, parser):
        """
            Initializes the reddit object.
            Params:
            -----
            parser: Config Parser Instance
        """
        # Setup Config
        self.parser = parser

        self.data_folder_path = Path(__file__) / self.parser.get('Output Config', 'data_path')

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
        self.credits = []
        self.thumbnails = []

        # Inform user of status
        print("Initialized Successfully!")

    def select_subreddits(self):
        """
        Selects the subreddits depending on the day
        Returns:
        -----
        subreddits: str, the list of concatenated subreddits for the day
        """
        # Get Content Config Info
        with open(self.data_folder_path / self.parser.get('Content Config', 'subreddits_list_location'),
                  encoding="utf8") as file:
            lines = file.readlines()

            # Get all the different "genres" of subreddits
            genre_counter = -1
            subreddit_genres = []
            for line in lines:
                if line.startswith("-----"):
                    genre_counter += 1
                    subreddit_genres.append("")
                    continue
                subreddit_genres[genre_counter] += line.rstrip() + "+"

            # Select a "genre" based on day
            today = datetime.today().weekday()
            return subreddit_genres[today]

    def scrape_posts(self):
        """
        Scrapes the posts from the subreddit and adds them to the list of posts
        """
        # Inform user of status
        print("Beginning to Scrape...")

        subreddits = self.select_subreddits()

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
            except TypeError:
                print("Skipping Non-Video / Non-Reddit Video...")
                continue

            # Filter out too long videos
            if submission_duration > max_submission_length:
                print("Skipping Long...")
                continue

            # Video Matched Criteria => Add to list
            curr_duration += submission_duration
            self.video_urls.append(submission.url)
            self.credits.append(submission.author.name)
            self.thumbnails.append(submission.preview['images'][0]['source']['url'])

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

    def get_credits(self):
        """
        Returns the names of the poster whose posts were downloaded
        Returns:
        -----
        self.credits: list, a list of the names of the user's whose videos were downloaded
        """
        return self.credits

    def get_thumbnails(self):
        """
        Returns the collected thumbnail URLs
        Returns:
        -----
        self.thumbnails: list, a list of the urls for possible thumbnails
        """
        return self.thumbnails
