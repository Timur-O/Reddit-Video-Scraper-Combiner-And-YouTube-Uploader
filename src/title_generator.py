import random
import configparser
from pathlib import Path


class TitleGenerator:
    def __init__(self):
        # Setup Config
        configFilePath = "config.txt"
        self.parser = configparser.ConfigParser()
        self.parser.read_file(open(configFilePath, "r"))

        self.data_folder_path = Path(__file__) / self.parser.get('Output Config', 'data_path')

        with open(self.data_folder_path / self.parser.get('Title Generation Config', 'adjectives_path')) as file:
            lines = file.readlines()
            self.adjectives = [line.rstrip() for line in lines]
            file.close()

        with open(self.data_folder_path / self.parser.get('Title Generation Config', 'video_words_path')) as file:
            lines = file.readlines()
            self.video_words = [line.rstrip() for line in lines]
            file.close()

        with open(self.data_folder_path / self.parser.get('Title Generation Config', 'people_path')) as file:
            lines = file.readlines()
            self.people = [line.rstrip() for line in lines]
            file.close()

        with open(self.data_folder_path / self.parser.get('Title Generation Config', 'verbs_path')) as file:
            lines = file.readlines()
            self.verbs = [line.rstrip() for line in lines]
            file.close()

        with open(self.data_folder_path / self.parser.get('Title Generation Config', 'locations_path')) as file:
            lines = file.readlines()
            self.locations = [line.rstrip() for line in lines]
            file.close()

    def generate(self):
        title = ""
        title += self.adjectives[int(random.uniform(0, 1) * len(self.adjectives))] + " "
        title += self.video_words[int(random.uniform(0, 1) * len(self.video_words))] + " "
        title += self.people[int(random.uniform(0, 1) * len(self.people))] + " "
        title += self.verbs[int(random.uniform(0, 1) * len(self.verbs))] + " in "
        title += self.locations[int(random.uniform(0, 1) * len(self.locations))] + " "
        return title
