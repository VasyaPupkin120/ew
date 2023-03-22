import urwid
import pdb
from urwid.main_loop import ExitMainLoop

# палитра
palette = [('I say', 'default,bold', 'default'),]
# создание главного цикла с просто заполняющим экран виджетом
mainloop = urwid.MainLoop(urwid.SolidFill("#"))
# предыдущее окно, не знаю зачем запоминать - вдруг пригодится когда нибудь.
prev_widget = None


def exitEW(*args, **kwargs):
    raise ExitMainLoop


def widget_substitution(*args, **kwargs):
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
    with open("log.txt", "a") as file:
        print("try detect paramters", file=file)
        print("\nargs:", args, "\nkwargs:", kwargs, file=file)

    prev_widget = args[0]
    if type(args[0]) == urwid.Button:
        mainloop.widget = args[-1]["new_widget"]
    if type(args[0]) == urwid.RadioButton:
        args[0].set_state(False)
        mainloop.widget = args[-1]["new_widget"]


class ExitWin(urwid.Overlay):
    """
    Окно подтверждения выхода.
    """
    def __init__(self):
        question = urwid.Text("Действительно выйти?")
        self.buttonExit = urwid.Button("Да", on_press=exitEW)
        self.buttonReturn = urwid.Button("Нет")
        pile = urwid.Pile([question, self.buttonExit, self.buttonReturn])
        body = urwid.SimpleFocusListWalker([pile,])
        body = urwid.ListBox(body)
        super().__init__(
            top_w=body,
            bottom_w=urwid.SolidFill(u'\N{MEDIUM SHADE}'),
            align=urwid.CENTER,
            width=(urwid.RELATIVE, 60),
            valign=urwid.MIDDLE,
            height=(urwid.RELATIVE, 60),
            min_width=20,
            min_height=9,)


class MainMenuWin(urwid.Overlay):
    """
    Окно главного меню.
    """
    def __init__(self):
        menu = []
        self.buttonTrain = urwid.Button(label="Тренировка")
        self.buttonTest = urwid.Button(label="Тестирование")
        self.buttonSettings = urwid.Button(label="Настройки")
        self.buttonExit = urwid.Button(label="Выход")
        menu.extend([self.buttonTrain, self.buttonTest, self.buttonSettings, self.buttonExit])
        menu = urwid.Pile(menu)
        body = urwid.SimpleFocusListWalker([menu,])
        body = urwid.ListBox(body)
        super().__init__(
            top_w=body,
            bottom_w=urwid.SolidFill(u'\N{MEDIUM SHADE}'),
            align=urwid.CENTER,
            width=(urwid.RELATIVE, 60),
            valign=urwid.MIDDLE,
            height=(urwid.RELATIVE, 60),
            min_width=20,
            min_height=9,)



# class ExitTextWidget(urwid.Edit):
#     """
#     Класс, который позволяет выйти из программы или вернуться обратно 
#     на предыдущее меню.
#     """
#     def __init__(self, caption, mainloop, save_widget):
#         self.mainloop = mainloop
#         self.save_widget = save_widget
#         super().__init__(caption=caption, edit_text='y')
#
#     def keypress(self, size, key):
#         """
#         Для выхода просто выбрасываем исключение, если передумали выходить -
#         то данный виджет (Exit) обратно подменяется заранее сохраненным save_widget
#         """
#         if key not in ('enter', 'esc') :
#             super().keypress(size, key)
#         else:
#             if self.edit_text in ("n", "N") or key == 'esc':
#                 self.mainloop.widget = self.save_widget
#             elif self.edit_text in ("y", "Y"):
#                 raise urwid.ExitMainLoop



def main():
    # окна и главный цикл - глобальные переменные
    global exit_window
    global mainmenu_window
    global mainloop

    # создание всех окон
    exit_window = ExitWin()
    mainmenu_window = MainMenuWin()

    # Подсоединяем сигналы. Если присоединять сигналы при определении классов,
    # то возникают проблемы что виджет главного цикла подменяется не нужным виджетом, 
    # а пустым виджетом-заглушкой.
    # Окно_главного_меню.Кнопка_запроса_окна_выхода_из_программы -> Окно_подтверждения_выхода_из_программы
    keyGoToExitWindow = urwid.connect_signal(
            mainmenu_window.buttonExit,
            "click",
            widget_substitution,
            user_arg={"new_widget": exit_window,}
            )
    # Окно_подтверждения_выхода_из_программы.Радиокнопка_возврата_в_программу -> Окно_главного_меню
    keyNoExit = urwid.connect_signal(
            exit_window.buttonReturn,
            "click",
            widget_substitution,
            user_arg={"new_widget": mainmenu_window,})

    mainloop.widget = mainmenu_window
    mainloop.run()


if __name__ == "__main__":
    main()
