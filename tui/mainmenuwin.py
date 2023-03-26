"""
Окно главного меню.
"""

import urwid

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

    def widget_substitution(self, substitution, mainloop):
        """
        Получает ссылки на новый виджет и главный цикл, после чего 
        подменяет виджет в главном цикле.
        """
        mainloop.widget = substitution




