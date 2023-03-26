"""
У каждого класса окна есть метод для подмены виджета в главном цикле.
Этот метод может вызвыаться по перехвату сигнала от виджета и с помощью 
значений параметров подменять виджет в главом цикле.

"""

import urwid
from urwid.main_loop import ExitMainLoop

from tui.exitwin import ExitWin
from tui.mainmenuwin import MainMenuWin
from tui.testwin import TestWin 
from tui.trainwin import TrainWin

# палитра
palette = [('I say', 'default,bold', 'default'),]
# создание главного цикла с просто заполняющим экран виджетом
mainloop = urwid.MainLoop(urwid.SolidFill("#"))
# предыдущее окно, не знаю зачем запоминать - вдруг пригодится когда нибудь.
prev_widget = None


def handler_buttons_exitwin(*args):
    """
    Обработчик двух кнопок на экране подтверждения выхода.
    """
    if args[0].get_label() in ["Yes", "Да"]:
        exit_window.exitEW()
    elif args[0].get_label() in ["No", "Нет"]:
        exit_window.widget_substitution(substitution=mainmenu_window, mainloop=mainloop)


def handler_edit_testingwin(*args):
    """
    Обработчик сигнала от поля ввода из окна тестирования.
    """
    if args[0].last_press == "esc":
        train_window.widget_substitution(substitution=mainmenu_window, mainloop=mainloop)
    if args[0].last_press == "enter":
        raise ExitMainLoop


def handler_edit_trainingwin(*args):
    """
    Обработчик сигнала от поля ввода из окна тренировки.
    """
    if args[0].last_press == "esc":
        train_window.widget_substitution(substitution=mainmenu_window, mainloop=mainloop)
    if args[0].last_press == "enter":
        train_window.compareInput()


def handler_buttons_mainmenuwin(*args):
    """
    Обработчик для нажатия всех кнопок в главном меню.
    Вызвает метод соответствующего окна для подмены этим окном виджета в главном цикле.
    """

    if args[0].get_label() in ["Training", "Тренировка"]:
        mainmenu_window.widget_substitution(substitution=train_window, mainloop=mainloop)
    elif args[0].get_label() in ["Testing", "Тестирование"]:
        mainmenu_window.widget_substitution(substitution=test_window, mainloop=mainloop)
    # elif args[0].get_label() in ["Options", "Опции"]:
    #     mainmenu_window.widget_substitution(substitution=train_window, mainloop=mainloop)
    elif args[0].get_label() in ["Exit", "Выход"]:
        mainmenu_window.widget_substitution(substitution=exit_window, mainloop=mainloop)


def linkSignals():
    """
    Присоединяет сигналы к всем кнопкам, у которых должны быть сигналы.
    К моменту вызова этой функции все окна уже созданы.
    """

    # Подсоединяем сигналы. Если присоединять сигналы при определении классов,
    # то возникают проблемы что виджет главного цикла подменяется не нужным виджетом, 
    # а созданным при определении класса пустым виджетом-заглушкой. Просто в 
    # момент определения одного класса, другие классы окон, нужные для присоединения
    # в качестве виджетов, еще не определены. И так перекрестно. Поэтому сначала 
    # заглушка на виджеты и отсуствие сигналов, а потом нормальные виджеты 
    # и присоединение сигналов.

    # exitwin.py - окно подтверждения выхода.
    # Для обоих кнопок один и тот же обработчик.
    handlerButtonReturnToMainMenu = urwid.connect_signal(
            exit_window.buttonReturn,
            "click",
            handler_buttons_exitwin,
            )
    handlerButtonExitWin = urwid.connect_signal(
            exit_window.buttonExit,
            "click",
            handler_buttons_exitwin,
            )

    # mainnemuwin.py - окно главного меню
    # один обработчик для всех кнопок главного меню
    handlerButtonGoToTraininWin = urwid.connect_signal(
            mainmenu_window.buttonTrain,
            "click",
            handler_buttons_mainmenuwin,
            )
    handlerButtonGoToTestingWin = urwid.connect_signal(
            mainmenu_window.buttonTest,
            "click",
            handler_buttons_mainmenuwin,
            )
    # handlerButtonGoToOptionsWin = urwid.connect_signal(
    #         mainmenu_window.buttonExit,
    #         "click",
    #         handler_buttons_mainmenuwin,
    #         )
    handlerButtonGoToExitWin = urwid.connect_signal(
            mainmenu_window.buttonExit,
            "click",
            handler_buttons_mainmenuwin,
            )

    # testwin.py - окно тестирования запомненности слов
    handlerEditTestingWin = urwid.connect_signal(
            test_window.edit_text,
            "change",
            handler_edit_testingwin,
            )

    # trainwin.py - окно тренировки
    handlerEditTrainingWin = urwid.connect_signal(
            train_window.edit_text,
            "change",
            handler_edit_trainingwin,
            )


def main():
    # окна и главный цикл - глобальные переменные
    global mainloop
    global train_window
    global test_window
    global exit_window
    global mainmenu_window

    # создание всех окон
    mainmenu_window = MainMenuWin()
    train_window = TrainWin()
    test_window = TestWin()
    exit_window = ExitWin()

    # подсоединение всех сигналов к всем кнопкам
    linkSignals()

    # запуск главного цикла
    mainloop.widget = mainmenu_window
    mainloop.run()


if __name__ == "__main__":
    main()
