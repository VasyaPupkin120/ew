"""
Модуль управляет пользователями - создает, изменяет, удаляет, формирует список пользователей.
Модуль, создает нового пользователя - конфиг, имя и полную структуру всех
имеющихся файлов с словами.
"""

import json
import shutil 
import datetime

import config

################################################################################
#                     блок создания пользователя                               #
################################################################################
def inuserdates(default: bool):
    """
    Здесь пользователь вводит данные об себе. Можно сгенерировать данные пользователя по умолчанию.
    """
    userdates = {}

    if default:
        userdates["username"] = "default"
        userdates["userdir"] = config.DIRPROJECT + "users/" + "default/"
        userdates["typetrain"] = config.RUS_TO_ENG
        return userdates

    # username
    username = input("tape your name: \n\t")

    # тип тестирования
    promptstr = "Выберите тип тренировки и тестирования:\n\t1: перевод русских слов на английский\n\t2: перевод английских слов на русский.\nПо умолчанию - русско-английский."
    num = input(promptstr)
    if  num == "1":
        typetrain =  config.RUS_TO_ENG
    elif num == "2":
        typetrain = config.ENG_TO_RUS
    else:
        typetrain = config.RUS_TO_ENG

    # директория которая будет выдана для пользователя
    userdir = config.DIRPROJECT + "users/" + username +"/"

    # итоговый результат
    userdates["username"] = username
    userdates["userdir"] = userdir
    userdates["typetrain"] = typetrain
    return userdates


def createfiles(userdates: dict):
    """
    Копирование всех файлов с словами из общего списка в директорию пользователя
    вместе с созданием самой директории пользователя.
    """

    # создание директории и копирование файлов с словами
    # userdir = "../users/" + userdates["username"] + "/phrases/"
    # dirwords = "../phrases"
    dirwords = config.DIRPROJECT + "phrases/"
    shutil.copytree(dirwords, userdates["userdir"] + "phrases/")

    # создание конфига пользователя
    userconf = {}
    # имя
    userconf["username"] = userdates["username"]
    # директория пользователя
    userconf["userdir"] = userdates["userdir"]
    # тип тренировки
    userconf["typetrain"] = userdates["typetrain"]
    # дата и время создания пользователя
    userconf["dtcreate"] = datetime.datetime.now() # нужно при сериализации указать параметр default=str
    # список файлов для тренировки
    userconf["fileswords"] = config.DICT_TRAIN_FILES
    # последний тренируемый файл
    userconf["lastfiletrain"] = config.DICT_TRAIN_FILES["default"]
    # количество тренируемых или тестируемых за один подход слов
    userconf["counttrywords"] = config.COUNT_TRY_WORDS
    # количество слов для запутывания
    userconf["countfakerec"] = config.COUNT_FAKE_REC

    # запись параметров в json-файл
    # default=str - для записи datetime-объекта в строковом виде
    jsonPath = userdates["userdir"] + userdates["username"] + ".json"
    with open(jsonPath, "w", encoding="utf-8") as json_file:
        json.dump(userconf, json_file, indent=4, ensure_ascii=False, default=str)


def create():
    """
    Создание пользователя.
    """
    while True:
        new_user = input("Создать нового пользователя (yes) или использовать дефолтного пользователя (no).\n")
        if new_user in ["yes", "Y", "y"]:
            userdata = inuserdates(default=False)
            break
        elif new_user in ["no", "N", "n"]:
            userdata = inuserdates(default=True)
            break
        else:
            continue
    createfiles(userdata)

    
def main():
    create()


if __name__ == "__main__":
    main()
