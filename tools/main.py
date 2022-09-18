from tools.reddit_tools import RedditTools


def main():
    # Delete All Saved => ie. all history for bot
    reddit_tools = RedditTools()
    reddit_tools.delete_all_saved()


if __name__ == "__main__":
    main()
