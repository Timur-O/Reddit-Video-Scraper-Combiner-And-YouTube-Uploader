import praw
import configparser


class RedditTools:
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

    def delete_all_saved(self):
        print("Starting unsave...")

        for i, saved_submission in enumerate(self.reddit.user.me().saved(limit=None)):
            saved_submission.unsave()
            print("Unsaved " + str(i) + " Submissions")

        print("Unsaved all successfully!")
