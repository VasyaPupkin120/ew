"""
Окно тренировки.
"""
import urwid
from . import mywidgets

words = {
    "0": {
        "rec_id": 0,
        "count_train_rus_to_eng": 0,
        "count_train_eng_to_rus": 0,
        "count_testing_rus_to_eng": 0,
        "count_testing_eng_to_rus": 0,
        "eng": "Hi.",
        "ru": "Привет." },
    "1": {
        "rec_id": 1,
        "count_train_rus_to_eng": 0,
        "count_train_eng_to_rus": 0,
        "count_testing_rus_to_eng": 0,
        "count_testing_eng_to_rus": 0,
        "eng": "Wow!",
        "ru": "Вот это да!" },
    }


class TrainWin(urwid.Overlay):
    """
    Окно тренировки.
    """
    def __init__(self):
        self.eng_text = urwid.Text(words["0"]["eng"])
        div_word = urwid.Divider(top=1, bottom=1)
        self.ru_text = urwid.Text(words["0"]["ru"])
        # виджет реакции верно/неверно
        self.congr_text = urwid.Text("...")
        div_block = urwid.Divider(div_char="-", top=3, bottom=3)
        self.edit_text = mywidgets.MyEdit()

        pile = urwid.Pile([
            self.eng_text,
            div_word, 
            self.ru_text,
            div_word, 
            self.congr_text,
            div_block,
            self.edit_text])

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

    def compareInput(self):
        if self.edit_text.get_edit_text() == words["0"]["eng"]:
            self.congr_text.set_text("Wow! Good!")
        else:
            self.congr_text.set_text("Oh, no. Very bad...")

    def widget_substitution(self, substitution, mainloop):
        """
        Получает ссылки на новый виджет и главный цикл, после чего 
        подменяет виджет в главном цикле.
        """
        mainloop.widget = substitution



