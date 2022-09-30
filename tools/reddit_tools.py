"""
File containing all the helpful tools for working with Reddit.
"""
import praw


class RedditTools:
    """
    The class containing all the helpful Reddit tools.
    """
    def __init__(self, parser):
        """
            Initializes the reddit object.
        """
        # Setup Config
        self.parser = parser

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
        """
        This method deletes all the saved posts in a Reddit account.
        """
        print("Starting unsave...")

        for i, saved_submission in enumerate(self.reddit.user.me().saved(limit=None)):
            saved_submission.unsave()
            print("Unsaved " + str(i) + " Submissions")

        print("Unsaved all successfully!")
