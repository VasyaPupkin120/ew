"""
Модуль, преобразующий сырой json файл с обоими переводами слов в пригодный 
для тренировки формат.
"""

import json

with open("rusengwords.json") as file:
    raw_dict = json.load(file)


out_dict = {}
count = 0
for eng_word, rus_word in raw_dict.items():
    eng_word = eng_word.strip()
    rus_word = rus_word.strip()
    out_dict[count] = {
            "rec_id": count,
            "count_train_rus": 0,
            "count_train_eng": 0,
            "count_testing_rus": 0,
            "count_testing_eng": 0,
            "eng": eng_word,
            "rus": rus_word,
            }
    count += 1


with open("default.json", "w") as file:
    json.dump(out_dict, file, ensure_ascii=False, indent=4)
