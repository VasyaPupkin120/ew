import urwid
import pdb
from urwid.main_loop import ExitMainLoop
from tui.exitwin import ExitWin
from tui.mainmenuwin import MainMenuWin
from tui.testwin import TestWin

# палитра
palette = [('I say', 'default,bold', 'default'),]
# создание главного цикла с просто заполняющим экран виджетом
mainloop = urwid.MainLoop(urwid.SolidFill("#"))
# предыдущее окно, не знаю зачем запоминать - вдруг пригодится когда нибудь.
prev_widget = None


def exitEW(*args, **kwargs):
    raise ExitMainLoop


def handlerMyEdit(*args):
    """
    Обработчик сигнала от поля ввода с фичами.
    """
    if args[0].last_press == "esc":
        widget_substitution(None, {"new_widget": mainmenu_window})
    if args[0].last_press == "enter":
        exitEW()




def widget_substitution(*args):
    """
    Подменяет виджет верхнего уровня в главном цикле. В основном вызывающие виджеты 
    будут кнопками, но возможны варианты. У разных вызывающих виджетов - разное 
    общее количество аргументов, но первый аргумент - всегда вызвающий виджет, 
    а последний - то, что было передано через параметр user_data при использовании
    connect_signal().
    """
    # переменная главного цикла
    global mainloop
    # переменная для глобального отслеживания какой виджет был предыдущим
    global prev_widget
    prev_widget = args[0]
    if type(args[0]) == urwid.RadioButton:
        # FIXME - не работает установка в False, разобраться как именно это сделать
        #  - чтобы выбранный вариант радиокнопки после исползования сбрасывался
        args[0].set_state(False)
        mainloop.widget = args[-1]["new_widget"]
    else:
        mainloop.widget = args[-1]["new_widget"]


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

    # exitwin.py - окно подтверждения выхода
    keyReturnToMainMenu = urwid.connect_signal(
            exit_window.buttonReturn,
            "click",
            widget_substitution,
            user_arg={"new_widget": mainmenu_window,},
            )
    keyExitToTerminal = urwid.connect_signal(
            exit_window.buttonExit,
            "click",
            exitEW,
            )

    # mainnemuwin.py - окно главного меню
    keyGoToExitWindow = urwid.connect_signal(
            mainmenu_window.buttonExit,
            "click",
            widget_substitution,
            user_arg={"new_widget": exit_window,},
            )
    keyGoToTestWindow = urwid.connect_signal(
            mainmenu_window.buttonTest,
            "click",
            widget_substitution,
            user_arg={"new_widget": test_window,},
            )

    # testwin.py - окно тестирования запомненности слов
    keyGoToMainMenu = urwid.connect_signal(
            test_window.edit_text,
            "change",
            handlerMyEdit,
            )


def main():
    # окна и главный цикл - глобальные переменные
    global exit_window
    global mainmenu_window
    global mainloop
    global test_window

    # создание всех окон
    exit_window = ExitWin()
    mainmenu_window = MainMenuWin()
    test_window = TestWin()

    # подсоединение всех сигналов к всем кнопкам
    linkSignals()

    # запуск главного цикла
    mainloop.widget = mainmenu_window
    mainloop.run()


if __name__ == "__main__":
    main()
