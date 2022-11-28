"""
Преобразовывает, стандартизирует txt файл из блоков с русско-английскими фразами, объединенными
построчно, блоки разделяются через пустую строку:

Hi.
Привет.

Wow!
Вот это да!
"""
import json

all_dict = {}

name_file = "default"
name_file_txt = name_file + ".txt"
# name_file_txt = "block_0001.txt"
name_file_json = name_file + ".json"

with open(name_file_txt, "r") as open_file:
    """
    Подсчитываем блоки, каждая пустая строка - новый блок. Флаг нужен для
    навигации внутри блока.

    в одну запись-словарь добавляются id записи, количество попыток изучения 
    данной записи в режиме rus-to-eng и eng-to-rus, количество успешных 
    тренировок данной записи в обоих режимах.
    """

    count_blocks = 0
    flag_lang = "eng"

    for line in open_file:
        str_count_blocks = str(count_blocks)
        if line.strip() == "": # создание нового блока + переключение флага
            all_dict[str_count_blocks] = {}
            all_dict[str_count_blocks]["rec_id"] = count_blocks
            all_dict[str_count_blocks]["count_train_rus_to_eng"] = 0
            all_dict[str_count_blocks]["count_train_eng_to_rus"] = 0
            all_dict[str_count_blocks]["count_testing_rus_to_eng"] = 0
            all_dict[str_count_blocks]["count_testing_eng_to_rus"] = 0
            flag_lang = "eng"
            continue
        if flag_lang == "eng": # если на строке с англ. фразой
            all_dict[str_count_blocks]["eng"] = line.strip()
            flag_lang = "ru"
            continue
        if flag_lang == "ru": # если на строке с русской фразой + окончание блока
            all_dict[str_count_blocks]["ru"] = line.strip()
            flag_lang = "eng"
            count_blocks += 1
            continue

# запись в json-файл
jsonStr = json.dumps(all_dict)
with open(name_file_json, "w", encoding="utf-8") as json_file:
    json_file.write(jsonStr)


