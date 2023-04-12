"""
Выделяем попарное пересечение слов из всех json-файлов в текущей директории.
Создаем итоговый файл с суммой всех пересечений.

Итоговый файл разбит на блоки до 5000 символов, чтобы можно было вставить в гугл-переводчик.
Нужно сначала дополнительно перенести все блоки json-файла на новые строки, 
сделать копию файла для русских значений, каждую строку с списокм слов вручную 
перевести и заменить.

"""

import json
import os

currdir = os.getcwd()
list_files = os.listdir(currdir)
list_jsons_names = []
for filepath in list_files:
    if filepath.endswith(".json") and filepath.startswith("words_"):
        list_jsons_names.append(filepath)


sets_books_texsts = []
for book in list_jsons_names:
    with open(book) as file:
        sets_books_texsts.append(set(json.load(file)))

# попарные пересечения всех книг
intersect_list = []
for index, book in enumerate(sets_books_texsts):
    for i in range(index+1, len(sets_books_texsts)):
        intersect = book.intersection(sets_books_texsts[i])
        intersect_list.append(intersect)

full_intersect = set()
for set_words in intersect_list:
    full_intersect = full_intersect.union(set_words)

full_intersect = list(full_intersect)
full_intersect.sort()

# text = '" "'.join(full_intersect)
list_words_5000 = []
list_texts = []

while True:
    for index_word, word in enumerate(full_intersect):
        # длина с учетом длин всех слов, двух кавычек и запятой и чуть запаса в 50 символов
        len_5000 = len("\n".join(list_words_5000)) + len(list_words_5000)*3 + 50
        if len_5000 >= 5000:
            break
        list_words_5000.append(word)
        index = index_word
    list_texts.append(list_words_5000)
    full_intersect = full_intersect[index:]
    list_words_5000 = []
    if index == len(full_intersect) - 1:
        break

with open("full_intersect_eng.json", "w") as file:
    json.dump(list_texts, file, ensure_ascii=False, default=str)
