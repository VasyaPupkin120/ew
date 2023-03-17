"""
Модуль отображения всего
"""

import time
import os
import usercreate
import curses, _curses
import pyfiglet
import locale


FPS = 1 / 10


def retlinewords(words: tuple) -> tuple:
    """
    Получает 15 + 1 слов (запутывающих и одно тренировочное),
    возвращает четыре строки, собранных из них
    """
    for i in range(4):
        str0 = words[i]
        str1 = words[i+4]
        str2 = words[i+8]
        str3 = words[i+12]

    return (str0, str1, str2, str3)




def print_welcome(main_win: _curses.window):
    """
    Вывод на главный экран приветствия.
    """
    maxY = curses.LINES - 1
    maxX = curses.COLS - 1

    # распечатка красивого названия по центру с учетом реальной ширины и высоты букв
    imagestr = pyfiglet.figlet_format("Eng Words", font="speed", justify="center", width = maxX) 

    main_win.addstr((maxY // 2) - 4, 0, imagestr)
    #main_win.border()
    main_win.refresh()
    time.sleep(1)
    main_win.clear()


def print_info(main_win: _curses.window, user: str = "default", typetrain: str = "rus-to-eng"):
    """
    Информационное окно (главное) - граница, пользователь, команды по умолчанию.
    """
    maxY = curses.LINES - 1
    maxX = curses.COLS - 1

    struser = f"Пользователь: {user}   Тип тренировки: {typetrain} "

    #main_win.border()
    main_win.addstr(1, 1, " Тренировка с EngWords")
    xstruser = maxX - len(struser)
    main_win.addstr(1, xstruser , struser)

    strcommads = " Меню: Ctrl-X   Обучение: Ctrl-L   Тестирование: Ctrl-T   Настройки: Ctrl-S"
    main_win.addstr(maxY-1, 1, strcommads)
    main_win.refresh()


def init_contentwin():
    """
    Отображает окно с контентом - обучение, тестирование,
    настройки, статистика.
    """
    maxY = curses.LINES - 1
    maxX = curses.COLS - 1
    contentwin = curses.newwin(curses.LINES - 13, curses.COLS - 4, 4, 2)
    contentwin.border()
    contentwin.refresh()
    return contentwin
    

def init_inputwin():
    """
    Отображает окно с текстовым вводом
    """

    maxY = curses.LINES - 1
    maxX = curses.COLS - 1
    inputwin = curses.newwin(3, curses.COLS - 4, maxY - 6, 2)
    inputwin.border()
    inputwin.move(1, 1)
    inputwin.refresh()
    return inputwin

def restorewin(win: _curses.window):
    """
    Очищает содержимое окна, восстанавливает границы, переносит курсор в начало,
    применяет изменения.
    """
    win.clear()
    win.border()
    win.move(1, 1)
    win.refresh()







def main(main_win: _curses.window):
    """
    Отображение всего
    """
    # вроде нужна
    curses.start_color()
    # разрешить цвета по умолчанию
    curses.use_default_colors()
    # скрыть курсор
    curses.curs_set(0)

    # приветствие, граница, информация
    print_welcome(main_win)
    print_info(main_win)

    # инициализация окон контента и ввода
    contentwin = init_contentwin()
    inputwin = init_inputwin()

    # показать курсор
    curses.curs_set(2)

    # для работы строки ввода
    curses.echo(True)
    curses.nocbreak()
    

    # главный цикл
    while True:
        #time.sleep(FPS)

        #key = inputwin.getstr(1, 1).decode("utf-8").strip()
        #key = inputwin.get_wch(1, 1)
        key = str(inputwin.getstr())

        # баг - если ввести русский символ, удалить через Backpase, еще раз его ввести, еще раз удалить, то 
        # вместо удаления там появится половина байтовой строки. И спецсимволы типа стрелок или Home/End 
        # выводят свое сокращение
        # из-за дебильного ввода строки нужно реализовать посимвольный ввод
        # это связано с тем, что клавиша Backspace в методе getstr() удаляет только один однобайтовый символ
        # а в utf-8 русские символы минимум двухбайтные, и одно нажатие удаляет только первый
        # и после двух последовательных вводов и удалений остается один двухбайтный символ
        # котрый и выносит мозги.

        restorewin(inputwin)
        restorewin(contentwin)


        contentwin.addstr(1, 1, key)
        inputwin.refresh()
        contentwin.refresh()


    main_win.getch()


if __name__ == "__main__":
    curses.wrapper(main)
