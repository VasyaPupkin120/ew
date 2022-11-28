"""
Модуль, отвечающий за тестирование знания слов из выбранного файла.

"""

import random
import printstests
import loadrecs
import string
from config import DEFAULT_COUNT_TESTING_WORDS, DEFALUT_COUNT_FAKE_REC, ENG_TO_RUS, KEY_DEFAULT_FILE_TRAIN, RUS_TO_ENG, TYPE_TRAINING



def create_UNGRADES_dict_rec_for_testing(
        count_train_recs : int, 
        input_dict: dict,
        ) -> dict:
    """
    Создает словарь, записи которого будут тестироваться,
    записи выбираются случайно из большого входного словаря.
    Используется, если нужно протестировать некоторое 
    количество случайных фраз. Получает количество записей,
    которое необходимо протестировать и словарь из которых 
    можно выбрать.
    """
    if count_train_recs == 0:
        return input_dict

    list_keys_input_dict = list(input_dict.keys())
    out_dict = {}
    list_random_keys = []
    len_input_dict = len(input_dict)

    # сложная конструкция для получения списка уникальных ключей (а не повторяющихся)
    while len(list_random_keys) != count_train_recs:
        list_random_keys.append(list_keys_input_dict[random.randrange(len_input_dict - 1)])
        list_random_keys = list(set(list_random_keys))

    if count_train_recs == 1:
        return input_dict[list_random_keys[0]]

    for key in list_random_keys:
        out_dict[key] = input_dict[key]

    return out_dict


def create_GRADES_dict_rec_for_testing():
    """
    функция должна сгенерировать словарь тех слов, 
    которые пользователь еще пока не запомнил - значения 
    count_testing_rus_to_eng и count_testing_eng_to_rus не превысили
    порог, скажем в 10 для данного пользователя - значит пользователь 
    менее 10 раз правильно перевел данную фразу.
    """
    return("контроль запомненности слов пока не реализован")


def normalize(words: str) -> str:
    """
    Возвращает нормализованную строку -
    в нижнем регистре, без знаков пунктуации.
    """
    words = words.lower()
    words = ''.join(c for c in words if c not in string.punctuation)
    return words


def key_translate():
    """
    Возвращает аббревиатуру, в какой язык выполняется перевод
    для использования как ключ словаря записи.
    """
    if TYPE_TRAINING ==  RUS_TO_ENG:
        key = "eng"
    elif TYPE_TRAINING ==  ENG_TO_RUS:
        key = "ru"
    else:
        print("Некорректное направление перевода. Выход.")
        exit()
    return key


def key_this_traintype():
    """
    Возвращает аббревиатуру текущей тренировки,
    которую можно использовать как ключ словаря записи.
    """
    if TYPE_TRAINING ==  RUS_TO_ENG:
        key = "ru"
    elif TYPE_TRAINING ==  ENG_TO_RUS:
        key = "eng"
    else:
        print("Некорректное направление перевода. Выход.")
        exit()
    return key


def generate_dict_fake_recs(
        input_dict : dict,
        count_fake_recs : int,
        key_train_rec: str,
        ) -> dict:
    """
    Генерирует словарь с случано выбранными фразами для показа
    точно неверных вариантов, для тренировочного эффекта.
    """

    list_keys_input_dict = list(input_dict.keys())
    len_input_dict = len(input_dict)
    list_rand_keys = []
    list_normalize_fake_words = []
    out_dict = {}

    # создаем список ключей фейковых записей
    while len(list_rand_keys) < count_fake_recs:
        rand_key = list_keys_input_dict[random.randrange(len_input_dict - 1)]

        # если фейковый ключ уже есть в списке, то второй раз он тоже не нужен
        if rand_key in list_rand_keys:
            continue
        # обработка случая, когда в фейковый список оказалось вставлено слово из тренируемой записи
        # в этом случае оказывается два одинаковых слова, что точно не нужно
        if normalize(input_dict[rand_key][key_translate()]) == normalize(input_dict[key_train_rec][key_translate()]):
            continue
        # также нужно обработать возможность, когда в списке оказывается несколько одинаковых слов
        # в вручную заполненом файле словаря часто встречаются полностью одинаковые записи
        if normalize(input_dict[rand_key][key_translate()]) in list_normalize_fake_words:
                continue
        # кроме того, нужно избавиться от слов, которые могут звучать по разному но
        # на другом языке означть одно и то же - Hello! и Hi.
        # Разумеется полностью не избавиться, хотя бы грубо.
        # Если слово в текущем варианте тренировки равно возможному фейковому слову в том же режиме тренировки
        if normalize(input_dict[rand_key][key_this_traintype()]) == normalize(input_dict[key_train_rec][key_this_traintype()]):
            continue

        list_rand_keys.append(rand_key)
        list_normalize_fake_words.append(normalize(input_dict[rand_key][key_translate()]))

    for key in list_rand_keys:
        out_dict[key] = input_dict[key]

    return out_dict


def composite_faketrain_recs(
        fake_dict: dict,
        full_dict: dict,
        key_train_rec: str
        ) -> dict:
    """
    Возвращает словарь из нескольких запутывающих записей и 
    одной записи, которая тестируется. При этом выполняется
    сортировка ключей для перемещения ключа тестируемой записи
    куда нибудь в середину словаря - без этого тестируемая запись
    почти всегда где то в конце словаря.
    """
    list_keys = list(fake_dict.keys())
    list_keys.append(key_train_rec)
    list_keys.sort()
    out_dict = {}
    for key in list_keys:
        out_dict[key] = full_dict[key]
    return out_dict
    

def testing(
        mode_testing: str = "ungrades",
        key_file_train: str = KEY_DEFAULT_FILE_TRAIN, 
        count_train_recs: int = DEFAULT_COUNT_TESTING_WORDS,
        count_fake_recs: int = DEFALUT_COUNT_FAKE_REC,
        ):
    """
    Функция, сводящая воедно все. Распечатка приветсвтия, загрузка
    слов из файла, составление словаря с тестируемыми фразами,
    собственно тестирование каждой фразы из этого словаря с выводом 
    запутывающих вариантов, реакция на результат сравнения (заполнение
    конфига каждого пользователя,или ничегонеделание).
    """

    # приветствие перед началом тестирования
    printstests.print_welcome()

    # удобное и быстрое получение всех слов из файла
    all_phrases = loadrecs.load_phrases(key_file_train=key_file_train)
    if not all_phrases:
        print(f"Не получилось загрузить файл с ключом {key_file_train}")
        exit()

    # составляем словарь из фраз, которые будут тестироваться.
    # режим тестирования mode_testing - это либо тестирование 
    # случайных фраз файла без опоры на количество правильных ответов 
    # либо тестирование только определенных слов, тестирование которых 
    # для данного пользователя еще пока не достигло значения, по которому 
    # можно сказать что пользователь запомнил слово.
    # возможно еще придумаются способы формирования слооваря для тренировки
    # если передан параметр fullfile, то значит, нужно тестировать весь файл
    # без разбиения на куски
    if mode_testing == "ungrades":
        dict_train_phrases = create_UNGRADES_dict_rec_for_testing(
                count_train_recs=count_train_recs,
                input_dict=all_phrases
                )
    elif mode_testing == "fullfile":
        dict_train_phrases = all_phrases
    elif mode_testing == "grades":
        print("Функция create_GRADES_dict_rec_for_testing() еще не реализована")
        exit()
    else:
        print("Не получилось сформировать словарь тестируемых фраз.\
                Не задан режим формирования этого словаря.")
        exit()

    # для каждой фразы из словаря для тренировки формируется новый 
    # словарь, содержащий одну тренировочную фразу и несколько 
    # фраз для запутывания. Данный словарь и ключ тренировочной записи 
    # передается на распечатку и там же сравнивается. Сюда должен возвращатся 
    # результат сравнения и уже здесь обрабатываться - типа только похвалить 
    # или еще приплюсовать очередной правильный ответ

    for key_train_rec in dict_train_phrases:
        fake_dict = generate_dict_fake_recs(
                input_dict=all_phrases,
                count_fake_recs=count_fake_recs,
                key_train_rec = key_train_rec,
                )
        full_train_dict = composite_faketrain_recs(
                fake_dict=fake_dict,
                full_dict=all_phrases,
                key_train_rec=key_train_rec,
                )
        # FIXME на основе result можно инкрементировать счетчик правильных результатов теста
        result = printstests.prints_and_return_compare(
                full_train_dict=full_train_dict,
                key_train_rec=key_train_rec,
                )
        

if __name__ == "__main__":
    testing()
