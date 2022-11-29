"""
Модуль возвращает путь к файлу на основе ключа этого файла
Может возвращать путь к случайно выбранному файлу или к файлу по умолчанию
"""

import random
from config.config import DICT_PATHS_TRAIN_FILES, KEY_DEFAULT_FILE_TRAIN, LIST_KEYS_DICT_PATHS_TRAIN_FILES



def default_path() -> str:
    return DICT_PATHS_TRAIN_FILES[KEY_DEFAULT_FILE_TRAIN]


def random_path() -> str:
    """
    Возвращает путь к случайно выбранному файлу из списка файлов.
    """
    if len(LIST_KEYS_DICT_PATHS_TRAIN_FILES) == 0:
        print("None train files in dict of files. Add link of one file.") 
        exit()
    elif len(LIST_KEYS_DICT_PATHS_TRAIN_FILES) == 1:
        return DICT_PATHS_TRAIN_FILES[LIST_KEYS_DICT_PATHS_TRAIN_FILES[0]]
    else:
        random_key = LIST_KEYS_DICT_PATHS_TRAIN_FILES[
                random.randrange(len(LIST_KEYS_DICT_PATHS_TRAIN_FILES) - 1)]
        return DICT_PATHS_TRAIN_FILES[random_key]


def key_path(key_file) -> str:
    return DICT_PATHS_TRAIN_FILES[key_file]


def return_path(key_file: str) -> str:
    """
    Осноная функция.
    На основании параметра-ключа выдает путь к файлу с словами.
    """
    if (not key_file) or (key_file == "default"):
        return default_path()
    elif (key_file == "random"):
        return random_path()
    elif (key_file in LIST_KEYS_DICT_PATHS_TRAIN_FILES):
        return key_path(key_file)
    else:
        print("Incorrect key file. Aborting.")
        exit()
