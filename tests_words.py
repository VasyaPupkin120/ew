"""
Модуль, отвечающий за тестирование знания слов из выбранного файла.

"""

import random
import printstests
import loadrecs
from config import DEFAULT_COUNT_TESTING_WORDS, DEFALUT_COUNT_FAKE_REC, KEY_DEFAULT_FILE_TRAIN



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


def generate_dict_fake_recs(
        input_dict : dict,
        count_fake_recs : int,
        ) -> dict:
    """
    Генерирует словарь с случано выбранными фразами
    для показа точно неверных вариантов, для тренировочного
    эффекта.
    """

    list_keys_input_dict = list(input_dict.keys())
    len_input_dict = len(input_dict)
    list_rand_keys = []
    out_dict = {}

    for i in range(count_fake_recs):
        list_rand_keys.append(list_keys_input_dict[random.randrange(len_input_dict - 1)])

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
        print(create_GRADES_dict_rec_for_testing())
        exit()
    else:
        print("Не получилось сформировать словарь тестируемых фраз.\
                Не задан режим формирования этого словаря.")
        dict_train_phrases = {}
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
