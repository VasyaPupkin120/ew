"""
Создание и соединение сигналами всех окон.
"""

import urwid
from urwid.main_loop import ExitMainLoop

from tui.win_exit import ExitWin
from tui.win_mainmenu import MainMenuWin
from tui.win_test import TestWin 
from tui.win_train import TrainWin
from tui.win_users import UsersWin


def main():

    # палитра
    palette = [('I say', 'default,bold', 'default'),]
    # создание главного цикла с просто заполняющим экран виджетом-заглушкой
    mainloop = urwid.MainLoop(urwid.SolidFill("#"), palette=palette)

    # создание всех окон
    mainmenu_window = MainMenuWin()
    train_window = TrainWin()
    test_window = TestWin()
    exit_window = ExitWin()
    users_window = UsersWin()


    # подсоединение всех сигналов в окнах
    # Если присоединять сигналы сразу при создании классов окон,
    # то возникают проблемы что виджет главного цикла подменяется не нужным виджетом, 
    # а созданным при определении класса пустым виджетом-заглушкой. Просто в 
    # момент определения одного класса, другие классы окон, нужные для присоединения
    # в качестве виджетов, еще не определены. И так перекрестно. Поэтому сначала 
    # заглушка на виджеты и отсуствие сигналов, а потом нормальные виджеты 
    # и присоединение сигналов.
    exit_window.link_signals(
            mainmenu_window=mainmenu_window,
            mainloop=mainloop,
            )
    mainmenu_window.link_signals(
            train_window=train_window,
            test_window=test_window,
            users_window=users_window,
            exit_window=exit_window,
            mainloop=mainloop,
            )
    train_window.link_signals(
            mainmenu_window=mainmenu_window,
            mainloop=mainloop,
            )
    test_window.link_signals(
            mainmenu_window=mainmenu_window,
            mainloop=mainloop,
            )

    # запуск главного цикла
    # mainloop.widget = mainmenu_window
    # для отладки будет пока другое окно
    mainloop.widget = train_window
    mainloop.run()


if __name__ == "__main__":
    main()
