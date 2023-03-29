"""
Окно выбора, создания, удаления пользователей.
"""


import urwid

class UsersWin(urwid.Overlay):
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

    def widget_substitution(self, substitution, mainloop):
        """
        Получает ссылки на новый виджет и главный цикл, после чего 
        подменяет виджет в главном цикле.
        """
        mainloop.widget = substitution

    # def get_path_to_users_dirs(self):


