"""
This file manages the generation of the titles.
"""
import random
from pathlib import Path


class TitleGenerator:
    """
    This class generates the titles.
    """
    def __init__(self, parser):
        # Setup Config
        self.parser = parser
        self.data_folder_path = Path(__file__) / self.parser.get('Output Config', 'data_path')

        self.replacement_dict = {}

        with open(self.data_folder_path / self.parser.get('Title Generation Config', 'formats_path'),
                  encoding="utf8") as file:
            lines = file.readlines()
            self.replacement_dict['formats'] = [line.rstrip() for line in lines]
            file.close()

        with open(self.data_folder_path / self.parser.get('Title Generation Config', 'adjectives_path'),
                  encoding="utf8") as file:
            lines = file.readlines()
            self.replacement_dict['adjectives'] = [line.rstrip() for line in lines]
            file.close()

        with open(self.data_folder_path / self.parser.get('Title Generation Config', 'video_words_path'),
                  encoding="utf8") as file:
            lines = file.readlines()
            self.replacement_dict['video_words'] = [line.rstrip() for line in lines]
            file.close()

        with open(self.data_folder_path / self.parser.get('Title Generation Config', 'people_path'),
                  encoding="utf8") as file:
            lines = file.readlines()
            self.replacement_dict['people'] = [line.rstrip() for line in lines]
            file.close()

        with open(self.data_folder_path / self.parser.get('Title Generation Config', 'verbs_path'),
                  encoding="utf8") as file:
            lines = file.readlines()
            self.replacement_dict['verbs'] = [line.rstrip() for line in lines]
            file.close()

        with open(self.data_folder_path / self.parser.get('Title Generation Config', 'locations_path'),
                  encoding="utf8") as file:
            lines = file.readlines()
            self.replacement_dict['locations'] = [line.rstrip() for line in lines]
            file.close()

    def generate(self):
        """
        Generates the title.
        Returns:
        -----
        title: str, the title
        """
        title = ""
        title_formats = self.replacement_dict.get("formats")
        title_format = title_formats[int(random.uniform(0, 1) * len(title_formats))]

        for word in title_format.split(" "):
            replacement_list = self.replacement_dict.get(word)
            if replacement_list is None:
                title += word + " "
            else:
                title += replacement_list[int(random.uniform(0, 1) * len(replacement_list))] + " "

        return title
