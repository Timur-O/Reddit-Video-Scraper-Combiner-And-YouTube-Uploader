"""
This file contains the main method which can run all the tools.
"""
import configparser
import argparse
from pathlib import Path

from tools.reddit_tools import RedditTools
from tools.youtube_utils import scrape_titles_from_channels


def main():
    """
    The main method from which you can easily run whichever tools are needed.
    """
    # Setup ArgParse
    arg_parser = argparse.ArgumentParser("tools.src")
    arg_parser.add_argument("unsave_tool", metavar="--unsave", default=False,
                        help="Indicates all saved posts should be deleted for the Reddit account in the config file.",
                            type=bool)
    arg_parser.add_argument("scrape_tool", metavar="--scrape", default=False,
                        help="Indicates titles should be scraped from the channels provided in the config file.",
                            type=bool)
    args = arg_parser.parse_args()

    # Setup Config
    config_file_path = "../config.txt"
    parser = configparser.ConfigParser()
    with open(config_file_path, "r", encoding="utf8") as file:
        parser.read_file(file)

    # Delete All Saved => i.e. all history for bot
    if args.unsave_tool:
        reddit_tools = RedditTools(parser)
        reddit_tools.delete_all_saved()

    # Scrape video titles from a channel
    if args.scrape_tool:
        csv_location = Path(__file__) / parser.get('Title Generation Config', 'training_data_location')
        list_of_channels = parser.get('Title Generation Config', 'training_channel_ids').split(",")

        scrape_titles_from_channels(list_of_channels, csv_location)


if __name__ == "__main__":
    main()
