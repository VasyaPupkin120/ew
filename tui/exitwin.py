"""
класс окна подтверждения выхода из программы.
"""
import urwid

class ExitWin(urwid.Overlay):
    """
    Окно подтверждения выхода.
    """
    def __init__(self):
        question = urwid.Text("Действительно выйти?")
        self.buttonExit = urwid.Button("Да")
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

    def widget_substitution(self, substitution, mainloop):
        """
        Получает ссылки на новый виджет и главный цикл, после чего 
        подменяет виджет в главном цикле.
        """
        mainloop.widget = substitution

    def exitEW(self):
        """
        Выход в систему.
        """
        raise urwid.ExitMainLoop


