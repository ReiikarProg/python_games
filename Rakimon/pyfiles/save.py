# file to manage saving and loading

import pickle
import os


class SaveManager:

    def __init__(self, file_extension, save_folder):
        self.file_extension = file_extension
        self.save_folder = save_folder

    # method to save the given 'data' into the save_data folder as a .txt file called name.save
    def save_data(self, data, name):
        data_file = open(f"../{self.save_folder}/{name}{self.file_extension}", "wb")
        pickle.dump(data, data_file)

    # method to load the file name.save
    def load_data(self, name):
        data_file = open(f"../{self.save_folder}/{name}{self.file_extension}", "rb")
        data = pickle.load(data_file)
        return data

    def check_for_file(self, name): return os.path.exists(f"../{self.save_folder}/{name}{self.file_extension}")

    # same as save_data and load_data, but with lists, ie possibility to manage several files

    def load_game_data(self, files_to_load, default_data):
        variables = []
        for index, file in enumerate(files_to_load):
            if self.check_for_file(file):
                variables.append(self.load_data(file))
            else:
                variables.append(default_data[index])
        if len(variables) > 1:
            return tuple(variables)
        else:
            return variables

    def save_game_data(self, data_to_save, file_names):
        for index, file in enumerate(data_to_save):
            self.save_data(file, file_names[index])

