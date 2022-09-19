import shutil
import configparser
import random
import requests

from redvid import Downloader
from pathlib import Path
from PIL import Image, ImageEnhance


def download_all(videos: list):
    """
    Downloads all the videos at the URLs provided
    Params:
    -----
    videos: list, the list of URLs to download
    """
    configFilePath = "../config.txt"
    parser = configparser.ConfigParser()
    parser.read_file(open(configFilePath, "r"))

    data_folder_path = Path(__file__) / parser.get('Output Config', 'data_path')

    downloader = Downloader(max_q=True)
    downloader.path = str(data_folder_path)

    # Download all videos
    for i, video in enumerate(videos):
        downloader.url = video
        downloader.download()
        print("Downloaded Video #" + str(i + 1))

    # Remove Temporary Folder
    shutil.rmtree(str(data_folder_path / "redvid_temp"))

    print("Downloaded Successfully!")


def download_thumbnail(thumbnail_urls: list):
    """
    Download, Convert, Improve Thumbnail
    Params:
    -----
    thumbnail_urls: list, the list of thumbnail URLs for which one random one will be downloaded
    """
    configFilePath = "../config.txt"
    parser = configparser.ConfigParser()
    parser.read_file(open(configFilePath, "r"))

    data_folder_path = Path(__file__) / parser.get('Output Config', 'data_path')
    thumbnail_file = data_folder_path / parser.get('Output Config', 'output_thumbnail')

    # Download Image
    img_data = requests.get(thumbnail_urls[int(random.uniform(0, 1) * len(thumbnail_urls))]).content
    with open(str(thumbnail_file) + '.webp', "wb") as handler:
        handler.write(img_data)

    # Convert Image
    image = Image.open(str(thumbnail_file) + '.webp').convert("RGB")
    image.save(str(thumbnail_file), "jpeg")

    # Increase Contrast
    image = Image.open(str(thumbnail_file))
    fil = ImageEnhance.Contrast(image)
    image = fil.enhance(4)
    fil = ImageEnhance.Sharpness(image)
    image = fil.enhance(3)
    image.save(str(thumbnail_file), "jpeg")

    print("Created Thumbnail Successfully!")
