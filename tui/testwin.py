"""
Окно тестирования.
"""
import urwid
from . import mywidgets


def exitEW(*args, **kwargs):
    raise urwid.ExitMainLoop


def handlerMyEditTest(*args):
    """
    Обработчик сигнала от поля ввода из окна тестирования.
    """
    if args[0].last_press == "esc":
        widget_substitution(None, {"new_widget": mainmenu_window})
    if args[0].last_press == "enter":
        exitEW()


class TestWin(urwid.Overlay):
    """
    Окно тренировки.
    """
    def __init__(self):
        list_words = [
                ["Hello", "world", "train", "list",],
                ["some", "for", "upper", "dict",],
                ["button", "exit", "overlay", "window"],
                ["menu", "conspect", "terminal", "phrases"]
                ]

        list_columns = []
        for words in list_words:
            temp_texts = []
            for word in words:
                temp_texts.append(urwid.Text(word))
            list_columns.append(urwid.Columns(temp_texts))

        pile = urwid.Pile(list_columns)

        self.edit_text = mywidgets.MyEdit()
        pile = urwid.Pile([pile, self.edit_text])
        body = urwid.Filler(pile)
        super().__init__(
            top_w=body,
            bottom_w=urwid.SolidFill(u'\N{MEDIUM SHADE}'),
            align=urwid.CENTER,
            width=(urwid.RELATIVE, 100),
            valign=urwid.MIDDLE,
            height=(urwid.RELATIVE, 100),
            min_width=50,
            min_height=15,)
