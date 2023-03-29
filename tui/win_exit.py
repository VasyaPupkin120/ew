"""
класс окна подтверждения выхода из программы.
"""
import urwid

class ExitWin(urwid.Overlay):
    """
    Окно подтверждения выхода.
    """
    def __init__(self):
        question = "Действительно выйти?"
        self.buttonExit = urwid.Button("Да")
        self.buttonReturn = urwid.Button("Нет")
        pile = urwid.Pile([self.buttonExit, self.buttonReturn])
        body = urwid.SimpleFocusListWalker([pile,])
        body = urwid.ListBox(body)
        box = urwid.LineBox(body)
        padding = urwid.Padding(box, align=urwid.CENTER, width=9, min_width=9)
        box = urwid.LineBox(padding, title=question)
        padding = urwid.Padding(box, align=urwid.CENTER, width=len(question)+8, min_width=len(question)+8)
        filler = urwid.Filler(padding, valign=urwid.MIDDLE, height=6, min_height=6)
        box = urwid.LineBox(filler, title="Eng Words")
        super().__init__(
            top_w=box,
            bottom_w=urwid.SolidFill(u'\N{MEDIUM SHADE}'),
            align=urwid.CENTER,
            width=(urwid.RELATIVE, 100),
            valign=urwid.MIDDLE,
            height=(urwid.RELATIVE, 100),
            min_width=len(question)+8,
            min_height=6,)

    def handler_exit(self, *args):
        """
        Обработчик кнопки выхода в терминал.
        """
        raise urwid.ExitMainLoop()

    def handler_return(self, *args):
        """
        Обработчик кнопки возврата в главное меню. Получает ссылки на виджет 
        главного окна и на виджет главного цикла, после чего подменяет виджет 
        в главном цикле.
        """
        # я не понимаю почему, но если выполнять подсоединение сигналов находясь 
        # внутри класса, то в обработчик будет отправлен кортеж, в котором 
        # первым будут идти те данные, которые я пересылаю в обработчик 
        # (например словарь), а последним элементом будет ссылка на тот объект,
        # который сгенерировал сигнал (например, кнопка). А если сигнал 
        # присоединять из сторонней функции, то наоборот, первым - ссылка на 
        # объект, вторым - пользовательские данные.
        mainloop = args[0]["mainloop"]
        mainmenu_window = args[0]["mainmenu_window"]
        mainloop.widget = mainmenu_window

    def link_signals(self, **kwargs):
        """
        Устанавливает все сигналы, связанные с этим окном.
        """
        handlerButtonReturnToMainMenu = urwid.connect_signal(
                self.buttonReturn,
                "click",
                self.handler_return,
                user_args=[{"mainmenu_window": kwargs["mainmenu_window"], "mainloop": kwargs["mainloop"]},]
                )
        handlerButtonExit = urwid.connect_signal(
                self.buttonExit,
                "click",
                self.handler_exit,
                )
