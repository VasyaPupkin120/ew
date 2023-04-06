"""
Создание или загрузка класса пользователя.
К классу пользователя очень удобно привязать методы наподобие "получить 
10 самых неизученных слов" или "получить 9 слов для запутывания"

Этот модуль работает с директориями пользователей которые лежат в users/

имя пользователя - строка без слэша в конце
путь к пользователю - строка пути (с слэшэм в конце)
все остальные пути - также с слэшем в конце
"""

import os
import shutil
import json
import datetime

class User():
    def __init__(self, conf):
        self.path = conf["path"] # путь к главному модулю
        self.username = conf["lastuser"]
        self.usersdir = self.path + "users/" # путь к директории с пользователями
        self.userpath = self.usersdir + self.username + "/"

        # путь к последнему тренируемому файлу, задается в self.settraindict()
        self.pathtotrainfile = ""
        
        # проверка наличия дефолтного пользователя, при отсутствии - создание
        self.createdefaultuser()

        # если пользователь с таким именем не найден, 
        # то использовать пользователя по умолчанию
        if not os.path.isdir(self.userpath):
            # user not exists
            self.userpath = self.usersdir + "defaultuser/"
            self.username = "defaultuser"

        # загрузка конфига пользователя и последнего тренируемого файла
        self.userconf ={}
        self.traindict = {}
        self.setuserconf()
        self.settraindict()



    def createuser(self, nameuser:str, params: dict):
        """
        Создает директории и конфиг пользователя.
        """
        if not os.path.isdir(self.usersdir + nameuser + "/"):
            # директория пользователя и файлы с словами
            dirwords = self.path + "phrases/"
            userdir = self.usersdir + nameuser + "/" + "phrases/"
            shutil.copytree(dirwords, userdir)
            # конфиг пользователя
            userconf = {}
            userconf["username"] = params["username"]
            userconf["userdir"] = params["userdir"]
            userconf["typetrain"] = params["typetrain"]
            userconf["dtcreate"] = datetime.datetime.now() # нужно при сериализации указать параметр default=str
            userconf["lastfiletrain"] = params["lastfiletrain"]
            # количество тренируемых или тестируемых за один подход слов
            userconf["counttrywords"] = params["counttrywords"]
            # количество слов для запутывания
            userconf["countfakerec"] = params["countfakerec"]
            # запись параметров в json-файл
            # default=str - для записи datetime-объекта в строковом виде
            jsonPath = self.usersdir + nameuser + "/" + nameuser + ".json"
            with open(jsonPath, "w", encoding="utf-8") as json_file:
                json.dump(userconf, json_file, indent=4, ensure_ascii=False, default=str)

    def createdefaultuser(self):
        """
        Дефолтный пользователь должен существовать всегда.
        Если при старте программы его нет, то он создается.
        """
        defaultusername = "defaultuser"
        if not os.path.isdir(self.usersdir + defaultusername + "/"):
            params = {
                    "username": defaultusername,
                    "userdir": self.usersdir + defaultusername + "/",
                    "typetrain": "eng-to-rus",
                    "lastfiletrain": "default.json",
                    "counttrywords": 10,
                    "countfakerec": 9,
                    }
            self.createuser(defaultusername, params)


    def setuserconf(self):
        """
        Установка конфига пользователя из файла.
        """
        pathfile = self.userpath + self.username + ".json"
        with open(pathfile, "r", encoding="utf-8") as file:
            conf = json.load(file)
        self.userconf = conf


    def settraindict(self, namefile=None):
        """
        Создает словарь с словами тренировок на основе указанного файла. 
        Если файл не указан, то используется последний записанный в конфиг пользователя.
        """
        if not namefile:
            namefile = self.userconf["lastfiletrain"]
            self.pathtotrainfile = self.userpath + "phrases/" + namefile
        else:
            self.pathtotrainfile = self.userpath + "phrases/" + namefile
        with open(self.pathtotrainfile, "r", encoding="utf-8") as file:
            traindict = json.load(file)
        self.traindict = traindict

