# constanst-flags train
RUS_TO_ENG = "rus-to-eng"
ENG_TO_RUS = "eng-to-rus"

# варианты тренировки/тестирования
TYPE_TRAINING = RUS_TO_ENG
# TYPE_TRAINING = ENG_TO_RUS

# выбор ключа файла для тренировки/тестирования
KEY_DEFAULT_FILE_TRAIN = "default"

# режимы тестирования - с выставлением оценок или без выставления оценок
# пока не хочется усложнять, потом разберусь, нужно ли вообще
DICT_MODES_TESTING = {
        }

# директория с файлами для тренировок
TRAIN_PATH = "./phrases/"

# пути к файлам с наборами слов для тренировки/тестирования
# каждый файл имеет свой ключ, который выбирается 
# когда нужно потренировать/протестировать конкретный файл
DICT_PATHS_TRAIN_FILES = {
        "default": TRAIN_PATH + "default.json",
        "TRAIN_FILE_0001": TRAIN_PATH + "block_0001.json",
        }

# список ключей словаря, содержащего пути к всем файлам с наборами слов
LIST_KEYS_DICT_PATHS_TRAIN_FILES = list(DICT_PATHS_TRAIN_FILES.keys())

# количество слов, тестируемых за один подход
DEFAULT_COUNT_TESTING_WORDS = 10

# количество фейковых фраз
DEFALUT_COUNT_FAKE_REC = 9


