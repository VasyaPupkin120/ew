"""
Окно тренировки. Разбито на блок Учителя (вывод тренируемого слова, реакция на ввод) 
и на блок Ученика (ввод перевода тренируемого слова)
"""
import urwid
import random
from . import mywidgets

class TrainWin(urwid.Overlay):
    """
    Окно тренировки.
    """
    def __init__(self, user):
        self.user = user
        self.eng_text = ""
        self.ru_text = ""

        self.traindict = user.traindict

        self.engTextWidget = urwid.Text(self.eng_text, align=urwid.CENTER)
        self.ruTextWidget = urwid.Text(self.ru_text, align=urwid.CENTER)
        self.edit_text = mywidgets.MyEdit()

        # обновляем значения в блоке Учителя и в поле ввода, 
        #на данный момент они уже должны существовать
        self.updateBlockTeacher()

        div_word = urwid.Divider(top=1, bottom=1)
        # виджет реакции верно/неверно
        self.congr_text = urwid.Text("...", align=urwid.CENTER)
        div_block = urwid.Divider(div_char="-", top=3, bottom=3)

        pile = urwid.Pile([
            self.engTextWidget,
            div_word, 
            self.ruTextWidget,
            div_word, 
            self.congr_text,
            div_block,
            self.edit_text])
        body = urwid.Filler(pile)
        box = urwid.LineBox(body, title="Eng Words")
        super().__init__(
            top_w=box,
            bottom_w=urwid.SolidFill(u'\N{MEDIUM SHADE}'),
            align=urwid.CENTER,
            width=(urwid.RELATIVE, 100),
            valign=urwid.MIDDLE,
            height=(urwid.RELATIVE, 100),
            min_width=50,
            min_height=15,)


    def updateBlockTeacher(self):
        """
        Обновление блока окна, отвечающего за показ тренируемого слова. 
        Назвал этот блок - Учителем
        """
        self.train_word = self.traindict[str(random.randrange(0, 176))]
        self.engTextWidget.set_text(self.train_word["eng"])
        self.ruTextWidget.set_text(self.train_word["ru"])
        # в этот момент нужно очистить поле ввода от предыдущего ввода
        # но если делать это через self.edit_text.set_edit_text(""), то 
        # возникнет сигнал и возникнет бесконечная рекурсия. 
        # Проблему не удалось решить созданием нового объкта MyEdit, определнием
        # новых методов, которые не вызывают генерацию сигнала (похоже наличие
        # сигнала нужно для обновления значения в виджете). Пробую на основе содержания
        # виджета ввода разделить на вариант без сравнения текста и с сравнением.
        # аналогичный set_edit_text, но не вызывающий генерацию сигнала
        # 
        # НАШЕЛ КОСЯК - НЕПОЛНО ОПРЕДЕЛЕЛИЛ ДЕЙСТВИЕ НАЖАТИЯ НА ЭНТЕР В КЕЙПРЕСС
        # Выглядело так, будо обращение к set_text() было два раза, сделал чтоб один.
        # Решил проблему в рекации на Enter в методе keypress(). 
        # Теперь нажатие на Enter сначала сохраняет текущее значение строки ввода а потом
        # просто очищает строку ввода.


    def train_logic(self):
        """
        Логика тренировки
        """
        #FIXME временно буду вводить только английские слова для тренировки.
        if self.edit_text.save_edit_text == self.train_word["eng"]:
            self.congr_text.set_text("Wow! Good!")
        else:
            self.congr_text.set_text("Oh, no. Very bad...")
        self.updateBlockTeacher()


    def handler_edit(self, *args):
        """
        Обработчик поля ввода. Получает ссылки на виджет главного цикла и на 
        виджет главного окна. В зависимости от последней управляющей кнопки
        выполняет логику тренировки или выходит в главное меню
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
            self.train_logic()

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
