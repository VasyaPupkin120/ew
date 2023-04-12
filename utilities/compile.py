"""
Объединяет русский и английский варианты для контроля и удобного отбора.
"""



import json
import os

# currdir = os.getcwd()
# list_files = os.listdir(currdir)
# list_jsons_names = []
# for filepath in list_files:
#     if filepath.endswith(".json") and filepath.startswith("full_") and ("rus" in filepath):
#         rus_words_path = filepath
#     if filepath.endswith(".json") and filepath.startswith("full_") and ("eng" in filepath):
#         eng_words_path = filepath

with open("full_intersect_rus.json") as file:
    rus_words = json.load(file)
with open("full_intersect_eng.json") as file:
    eng_words = json.load(file)

temp = []
for i in rus_words:
    temp.extend(i)
rus_words = temp

temp = []
for i in eng_words:
    temp.extend(i)
eng_words = temp

full_dict = {}

for index, word in enumerate(eng_words):
    full_dict[word] = rus_words[index] 

with open("rusengwords.json", "w") as file:
    json.dump(full_dict, file, indent=4, ensure_ascii=False)



