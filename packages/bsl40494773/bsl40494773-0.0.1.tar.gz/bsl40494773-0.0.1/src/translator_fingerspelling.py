# bsl_translator_fingerspelling

from training import train_model
from translate import translate
from dataset_creator import create_dataset_from


class FingerSpelling:

    def __init__(self):
        pass

    def create_dataset(self, data_path: str):

        if data_path == "":
            print("There was no data path provided")
            return None
        else:
            return create_dataset_from(data_path)

    def train_fingerspelling(self, data_pickle_path: str):
        if data_pickle_path == "":
            print("There was no data path provided")
            return None
        else:
            return train_model(data_pickle_path)

    def translate_sign(self, image_path):

        if image_path == "":
            print("There was no image path provided")
            return None
        else:
            return translate(image_path)
