"""
Окно главного меню.
"""

import urwid

class MainMenuWin(urwid.Overlay):
    """
    Окно главного меню.
    """
    def __init__(self):
        self.buttonTrain = urwid.Button(label="Тренировка", )
        self.buttonTest = urwid.Button(label="Тестирование")
        self.buttonSettings = urwid.Button(label="Настройки")
        self.buttonUsers = urwid.Button(label="Пользователи")
        self.buttonExit = urwid.Button(label="Выход")
        max_width_button_label = 12 + 4 # 4 - два пробела и две скобки вокруг названия кнопки

        self.paddingTrain = urwid.Padding(self.buttonTrain, align=urwid.CENTER, width=max_width_button_label)
        self.paddingTest = urwid.Padding(self.buttonTest, align=urwid.CENTER, width=max_width_button_label)
        self.paddingSettings = urwid.Padding(self.buttonSettings, align=urwid.CENTER, width=max_width_button_label)
        self.paddingUsers = urwid.Padding(self.buttonUsers, align=urwid.CENTER, width=max_width_button_label)
        self.paddingExit = urwid.Padding(self.buttonExit, align=urwid.CENTER, width=max_width_button_label)
        menu = [self.paddingTrain, self.paddingTest, self.paddingSettings, self.paddingUsers, self.paddingExit]
        menu = urwid.Pile(menu)
        body = urwid.SimpleFocusListWalker([menu,])
        body = urwid.ListBox(body)
        body = urwid.LineBox(body)
        body = urwid.LineBox(body, title="Меню")
        body = urwid.Padding(body, align=urwid.CENTER, width=20,)
        body = urwid.Filler(body, valign=urwid.MIDDLE, height=len(menu.contents)+4, min_height=len(menu.contents)+4,)
        body = urwid.LineBox(body, title="Eng Words")
        super().__init__(
            top_w=body,
            bottom_w=urwid.SolidFill(u'\N{MEDIUM SHADE}'),
            align=urwid.CENTER,
            width=(urwid.RELATIVE, 100,),
            # valign=urwid.MIDDLE,
            valign=(urwid.RELATIVE, 50,),
            height=(urwid.RELATIVE, 100,),
            min_width=20,
            min_height=11,)

    def widget_substitution(self, substitution, mainloop):
        """
        Получает ссылки на новый виджет и главный цикл, после чего 
        подменяет виджет в главном цикле.
        """
        mainloop.widget = substitution




