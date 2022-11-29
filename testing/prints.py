"""
Распечатка задания и распечатка списка возможных ответов.
rec - словарь (точнее - структура) фразы, со всеми переводами и доп. информацией
list_possible_rec - список случайно выбранных структур rec, 
answer - строка возможного ответа
answer_user - строка ответа пользователя
quest - строка, которую пользователю нужно перевести.
"""
from config.config import TYPE_TRAINING
from config.config import RUS_TO_ENG, ENG_TO_RUS


def print_welcome():
    """
    Приветствие.
    """
    print(f"\nНачало тестирования знания слов в режиме {TYPE_TRAINING}.")


def print_quest(key_train_rec: str, train_dict: dict):
    """
    Распечатка задания для перевода.
    """
    if TYPE_TRAINING == RUS_TO_ENG :
        print("\nПереведите предложенную фразу на английский:")
        print("\n\t", train_dict[key_train_rec]['ru'], sep="")
    elif TYPE_TRAINING == ENG_TO_RUS:
        print("\nПереведите предложенную фразу на русский:")
        print("\n\t", train_dict[key_train_rec]['eng'], sep="")
    else:
        print("Этого функционала еще нет.")
    print()


def print_one_answer(key_rec: str, full_dict: dict):
    """
    Распечатка только одного из вариантов перевода отдельной фразы.
    Важно: распечатывается именно вариант ответа а не вся структура-запись-словарь.
    """
    if TYPE_TRAINING == RUS_TO_ENG :
        print(full_dict[key_rec]['eng'], end="")
    elif TYPE_TRAINING == ENG_TO_RUS:
        print(full_dict[key_rec]['ru'], end="")
    

def print_possible_answers(dict_possible_recs: dict):
    """
    Распечатка пронумерованных вариантов ответа.
    """
    print("Варианты перевода:")
    for rec in dict_possible_recs:
        print("\t", end="")
        print_one_answer(key_rec=rec, full_dict=dict_possible_recs)
        print()


def input_user_answer() -> str:
    return input("\nНаберите перевод фразы: \n\n\t")


def compare_answer(answer: str, key_train_rec: str, train_dict: dict) -> bool:
    """
    Сравнение ответа пользователя и вариантов фразы в записи.
    """
    # лень писать кучу выборок, просто ответ сравнивается с 
    # обоими вариантами фразы. Стоит усложнить, убрать зависимость
    # от знаков пунктуации и регистра.
    if answer == train_dict[key_train_rec]['eng'] or answer == train_dict[key_train_rec]['ru']:
        return True
    return False


def prints_and_return_compare(full_train_dict: dict, key_train_rec: str):
    """
    Распечатывает все варианты ответов + тренируемую запись.
    Сравнивает введеный пользователем текст, возвращает 
    результат сравнения
    """
    print_quest(key_train_rec=key_train_rec, train_dict=full_train_dict)
    print_possible_answers(dict_possible_recs=full_train_dict)
    answer = input_user_answer()
    compare = compare_answer(answer=answer, key_train_rec=key_train_rec, train_dict=full_train_dict)
    if compare:
        print("\nВсе верно.")
        return(True)
    else:
        print("\nГде то ошибка")
        return(False)
