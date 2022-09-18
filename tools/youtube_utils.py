from pathlib import Path
import csv
import requests
from bs4 import BeautifulSoup


def scrape_youtube_titles(channel_id: str, save_location: Path):
    """
    Scrapes the titles of the videos from a channel
    Params:
    -----
    channel_id: str, the name of the channel to scrape the titles from
    save_location: Path, the location of the CSV to save the titles to
    Returns:
    -----
    titles: str, the list of video titles
    """
    titles = []

    print("Beginning to Scrape Titles...")

    url = "https://www.youtube.com/feeds/videos.xml?channel_id=" + channel_id
    html = requests.get(url)
    soup = BeautifulSoup(html.text, "lxml")
    for entry in soup.findAll("entry"):
        titles.append(entry.findNext("title").text)

    with open(save_location, 'a') as fd:
        for title in titles:
            try:
                fd.write(title + "\n")
            except Exception:
                continue

    print("Scraped Titles Successfully!")


def scrape_titles_from_channels(channels: list, save_location: Path):
    """
    Scrapes all the titles from the list of channels
    Params:
    -----
    channels: list, the list of channel ids for which to get the titles
    """
    for channel in channels:
        scrape_youtube_titles(channel, save_location)