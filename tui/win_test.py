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


    def testing_logic(self):
        """
        Логика тестирования
        """
        raise urwid.ExitMainLoop


    def handler_edit(self, *args):
        """
        Обработчик поля ввода в окне тестирования. Получает ссылки на виджет 
        главного цикла и на виджет главного окна. В зависимости от последней 
        управляющей кнопки выполняет логику тестирования или выходит в главное 
        меню
        """
        # я не понимаю почему, но если выполнять подсоединение сигналов находясь 
        # внутри класса, то в обработчик будет отправлен кортеж, в котором 
        # первым будут идти те данные, которые я пересылаю в обработчик 
        # (например словарь), а последним элементом будет ссылка на тот объект,
        # который сгенерировал сигнал (например, кнопка). А если сигнал 
        # присоединять из сторонней функции, то наоборот, первым - ссылка на 
        # объект, вторым - пользовательские данные.
        if args[1].last_press == "esc":
            mainloop = args[0]["mainloop"]
            mainmenu_window = args[0]["mainmenu_window"]
            mainloop.widget = mainmenu_window
        if args[1].last_press == "enter":
            self.testing_logic()

    def link_signals(self, **kwargs):
        """
        Устанавливает все сигналы, связанные с этим окном.
        """
        handlerEditTrainingWin = urwid.connect_signal(
                self.edit_text,
                "change",
                self.handler_edit,
                user_args=[{"mainloop": kwargs["mainloop"], "mainmenu_window": kwargs["mainmenu_window"]}, ]
                )
