"""
Модуль, создает нового пользователя - конфиг, имя и полную структуру всех
имеющихся файлов с словами.
"""
import json
import os
import random
import shutil

# user = {}
# username = ""
# user_id = -1
#
# user["username": username]
# user["user_id": user_id]

# словарь, содержащий оценки для каждого файла

# user_recs = {}

user = "Vasya"
useridir = "./" + user + str(random.randint(500, 999)) + "/"
dirwords = "/phrases/"




def get_filesword():
    """
    Копирование всех файлов с словами из общего списка в директорию пользователя
    вместе с созданием самой директории пользователя.
    """
    shutil.copytree(".." + dirwords, useridir + dirwords)

if __name__ == "__main__":
    get_filesword()
