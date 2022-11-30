"""
Модуль позволяет загружать из указанного json-файла все записи
и возвращать словарь.
"""

import json
#from . import getpath
import getpath
from ..config import *


def set_path_to_file(key: str) -> str:
    """
    Выбор файла для тестирования. Возвращает путь к файлу.
    """
    return getpath.return_path(key_file=key)


def load_phrases(key_file_train: str) -> dict:
    """
    Загрузка данных из файла и возврат в качестве словаря.
    Если файл не был загружен, завершается работа программы.
    Ответственность за проверку корректности непустого ключа лежит на 
    функции set_path_file_for_test (точнее на set_path.return_path). 
    Данная же функция передает в нее ключ без проверок.
    """
    if not key_file_train or key_file_train == KEY_DEFAULT_FILE_TRAIN):
        path_load_file = set_path_to_file(KEY_DEFAULT_FILE_TRAIN)
    elif (key_file_train == "random"):
        path_load_file = set_path_to_file("random")
    else:
        path_load_file = set_path_to_file(key_file_train)
    with open(path_load_file, encoding="utf-8") as words_json:
        dict_words = json.loads(words_json.read())
        return dict_words
    print("file not load. Sorry.")
    exit()
