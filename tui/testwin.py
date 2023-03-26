"""
Окно тренировки.
"""
import urwid
from . import mywidgets


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
            width=(urwid.RELATIVE, 60),
            valign=urwid.MIDDLE,
            height=(urwid.RELATIVE, 60),
            min_width=20,
            min_height=9,)
