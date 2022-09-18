import shutil
import configparser

from redvid import Downloader
from pathlib import Path


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

    if parser.get('Output Config', 'data_path') != '':
        data_folder_path = Path(parser.get('Output Config', 'data_path'))
    else:
        data_folder_path = Path(__file__).parent.parent / "data"

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
