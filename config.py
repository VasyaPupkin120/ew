# конфиг всей программы
import os

# директория проекта
DIRPROJECT = os.getcwd() + "/"

# constanst-flags train
RUS_TO_ENG = "rus-to-eng"
ENG_TO_RUS = "eng-to-rus"

# варианты тренировки/тестирования
TYPE_TRAINING = RUS_TO_ENG

# режимы тестирования - с выставлением оценок или без выставления оценок
# пока не хочется усложнять, потом разберусь, нужно ли вообще
DICT_MODES_TESTING = {
        }

# пути к файлам с наборами слов для тренировки/тестирования
# каждый файл имеет свой ключ, который выбирается 
# когда нужно потренировать/протестировать конкретный файл
DICT_TRAIN_FILES = {
        "default": "default.json",
        }

# список ключей словаря, содержащего пути к всем файлам с наборами слов
LIST_KEYS_DICT_PATHS_TRAIN_FILES = list(DICT_TRAIN_FILES.keys())

# количество слов, тренируемых или тестируемых за один подход
COUNT_TRY_WORDS = 10

# количество фейковых фраз
COUNT_FAKE_REC = 9


#git commit -m "переделал струтуру, убрал подпакеты, поддиректории, остались исключительно вспомогательные. Работоспособный код добавления нового пользователя"
