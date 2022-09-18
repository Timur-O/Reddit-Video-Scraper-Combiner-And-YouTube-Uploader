from pathlib import Path

import configparser


def create_model():
    configFilePath = "../config.txt"
    parser = configparser.ConfigParser()
    parser.read_file(open(configFilePath, "r"))

    # Load Data
    data_location = Path(__file__) / parser.get('Title Generation Config', 'training_data_location')
    model_location = Path(__file__) / parser.get('Title Generation Config', 'model_location')


def use_model(prompt: str, length: int):
    configFilePath = "../config.txt"
    parser = configparser.ConfigParser()
    parser.read_file(open(configFilePath, "r"))

    data_location = Path(__file__) / parser.get('Title Generation Config', 'training_data_location')
    model_location = Path(__file__) / parser.get('Title Generation Config', 'model_location')


