import configparser
from pathlib import Path

from src import title_generator
from tools.reddit_tools import RedditTools
from tools.youtube_utils import scrape_titles_from_channels


def main():
    # Delete All Saved => ie. all history for bot
    # reddit_tools = RedditTools()
    # reddit_tools.delete_all_saved()

    # Scrape video titles from a channel
    configFilePath = "../config.txt"
    parser = configparser.ConfigParser()
    parser.read_file(open(configFilePath, "r"))

    csv_location = Path(__file__) / parser.get('Title Generation Config', 'training_data_location')
    list_of_channels = parser.get('Title Generation Config', 'training_channel_ids').split(",")

    scrape_titles_from_channels(list_of_channels, csv_location)


if __name__ == "__main__":
    main()
