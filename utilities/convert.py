"""
Модуль получает список pdf книг, создает множество
использумых в книгах слов, сохраняет их в json.
"""

import pdftotext
import re
import json
import sys
import os


def replace_punctuation(line):
    """
    Получает весь текст книги. 
    Заменяет все посторонние символы на пробелы.
    """
    list_punctuation = [
            "\n", ")", "(", 
            ",", ".", "\"",
            "=", "{", "}", 
            "[", "]", "'",
            '"', '’', '/',
            '+', "\\", "*",
            "&", ":", ";",
            "<", ">", "^",
            ]
    for punc in list_punctuation:
        if punc in line:
            line = line.replace(punc, " ")
    return line

def notgoodline(some):
    """
    Исключает те слова, в которых найдены цифры, тире или подчеркивания.
    """
    for i in range(0, 10):
        if str(i) in some:
            return False
    if len(some) <= 2:
        return False
    if "_" in some:
        return False
    if "-" in some:
        return False
    return True


# получение имен файлов из аргументов командной строки, загрузка и преобразование в текст
names_files = sys.argv[1:]
if not names_files:
    print("need input files")
    exit()
list_texts_books = []
for file in names_files:
    with open(file, "rb") as file:
        pdf = pdftotext.PDF(file)
    pdf = "\n".join(pdf)
    list_texts_books.append(pdf)

# для текста каждой книги - выделение отдельных слов.
for index, text_book in enumerate(list_texts_books):
    text_book = replace_punctuation(text_book)
    list_raw_words = re.findall(r"\b[^ \n\t]*\b", text_book)
    list_raw_words = list(set(list_raw_words))
    list_true_words = []
    for raw_word in list_raw_words:
        if notgoodline(raw_word):
            list_true_words.append(raw_word.lower())
    list_true_words = list(set(list_true_words))
    list_true_words.sort()
    namefile = names_files[index].replace(".pdf", ".json").replace("books/", "")
    with open(namefile, "w") as file:
        json.dump(list_true_words, file, indent=4, ensure_ascii=False, default=str)

