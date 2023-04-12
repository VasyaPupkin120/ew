"""
Окно тренировки. Разбито на блок Учителя (вывод тренируемого слова, реакция на ввод) 
и на блок Ученика (ввод перевода тренируемого слова)
"""
import urwid
import random
import json
from . import mywidgets

class TrainWin(urwid.Overlay):
    """
    Окно тренировки.
    """
    def __init__(self, user):
        self.user = user

        self.traindict = user.traindict
        self.eng_text = ""
        self.rus_text = ""
        self.setNewTrainConcept()

        self.one_line = urwid.Divider()
        self.two_lines = urwid.Divider(bottom=1)
        self.tree_lines = urwid.Divider(top=1, bottom=1)
        
        self.all_modes_teacher = ["outruseng", "outengrus", "inrus", "ineng", "inrus1", "ineng1", "inrus2", "ineng2", "exit"]
        self.mode_teacher = "start"
        self.teacher = None
        # FIXME слегка странно выглядит оценка режима ineng2 которая выводится уже в режиме exit.
        # стоит создать отдельный виджет с всеми оценками где нибудь слева, в который будут вноситься оценки
        # по мере получения.
        self.grade_answer = urwid.AttrWrap(urwid.Text("...", align=urwid.CENTER, ), None ) 
        self.set_teacher()

        self.student = None
        self.set_student()

        pile = urwid.Pile([
            self.teacher,
            self.one_line,
            self.grade_answer,
            self.one_line,
            self.student,
            ])

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


    def setNewTrainConcept(self):
        """
        Задача этого метода - каким либо образом выбрать, какая пара слов
        будет тренироваться сейчас.
        """
        self.train_concept = self.traindict[str(random.randrange(0, 176))]
        self.eng_text = self.train_concept["eng"]
        self.rus_text = self.train_concept["rus"]
        # self.engTextWidget.set_text(self.train_concept["eng"])
        # self.ruTextWidget.set_text(self.train_concept["ru"])

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
        Логика тренировки. Тренируем одновременно оба направления.
        ТО есть после каждого нажатия Enter в поле ввода Ученика, 
        выполняется переход в этот метод и в зависимости от этапа Учителя
        либо вывод для запоминания, либо ожидание ввода от Ученика и оценка.
        """
        badanswer = urwid.Text([("badanswer", " -1 "), ], align=urwid.CENTER, )
        goodanswer = urwid.Text([("goodanswer", " +1 "), ], align=urwid.CENTER, )
        # FIXME выглядит лапшой, что нибудь придумать, типа отдельных классов для Учителя и Ученика

        # задаем вид учителя в зависимости от этапа тренировки
        if self.mode_teacher == "start":
            self.mode_teacher = "outruseng"
            self.set_teacher()
            return

        if self.mode_teacher == "outruseng":
            self.mode_teacher = "outengrus"
            self.set_teacher()
            return

        if self.mode_teacher == "outengrus":
            self.mode_teacher = "inrus"
            self.set_teacher()
            return

        if self.mode_teacher == "inrus":
            if self.student_edit_text.save_edit_text == self.rus_text:
                self.grade_answer.original_widget = goodanswer
                self.train_concept["count_train_rus"] += 1
            else:
                self.grade_answer.original_widget = badanswer
                self.train_concept["count_train_rus"] -= 1
            self.mode_teacher = "ineng"
            self.set_teacher()
            return

        if self.mode_teacher == "ineng":
            if self.student_edit_text.save_edit_text == self.eng_text:
                self.grade_answer.original_widget = goodanswer
                self.train_concept["count_train_eng"] += 1
            else:
                self.grade_answer.original_widget = badanswer
                self.train_concept["count_train_eng"] -= 1
            self.mode_teacher = "inrus1"
            self.set_teacher()
            return

        if self.mode_teacher == "inrus1":
            if self.student_edit_text.save_edit_text == self.rus_text:
                self.grade_answer.original_widget = goodanswer
                self.train_concept["count_train_rus"] += 1
            else:
                self.grade_answer.original_widget = badanswer
                self.train_concept["count_train_rus"] -= 1
            self.mode_teacher = "ineng1"
            self.set_teacher()
            return

        if self.mode_teacher == "ineng1":
            if self.student_edit_text.save_edit_text == self.eng_text:
                self.grade_answer.original_widget = goodanswer
                self.train_concept["count_train_eng"] += 1
            else:
                self.grade_answer.original_widget = badanswer
                self.train_concept["count_train_eng"] -= 1
            self.mode_teacher = "inrus2"
            self.set_teacher()
            return

        if self.mode_teacher == "inrus2":
            if self.student_edit_text.save_edit_text == self.rus_text:
                self.grade_answer.original_widget = goodanswer
                self.train_concept["count_train_rus"] += 1
            else:
                self.grade_answer.original_widget = badanswer
                self.train_concept["count_train_rus"] -= 1
            self.mode_teacher = "ineng2"
            self.set_teacher()
            return

        if self.mode_teacher == "ineng2":
            if self.student_edit_text.save_edit_text == self.eng_text:
                self.grade_answer.original_widget = goodanswer
                self.train_concept["count_train_eng"] += 1
            else:
                self.grade_answer.original_widget = badanswer
                self.train_concept["count_train_eng"] -= 1
            self.mode_teacher = "exit"
            self.set_teacher()
            return

        # выбор нового тренируемого слова и переход к его тренировке
        if self.mode_teacher == "exit":
            self.grade_answer.original_widget = urwid.Text("...", align=urwid.CENTER)
            self.mode_teacher = "outruseng"
            self.setNewTrainConcept()
            self.set_teacher()
            return




    def handler_edit(self, *args):
        """
        Обработчик сигнала от поля ввода. Получает ссылки на виджет главного цикла и на 
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
            with open(self.user.pathtotrainfile, "w") as file:
                json.dump(self.traindict, file, ensure_ascii=False, indent=4)
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
                self.student_edit_text,
                "change",
                self.handler_edit,
                user_args=[{"mainloop": kwargs["mainloop"], "mainmenu_window": kwargs["mainmenu_window"]}, ]
                )

    def set_teacher(self):
        """
        Формирует и отображает блок учителя. Тренировка каждого понятия 
        проходит в несколько этапов: 
            вывод русско-английского,
            вывод англо-русского,
            вывод только английского,
            вывод только русского,
            предложение ввести русское отображение понятия (с оценкой),
            предложение ввести английское отображение понятия (с оценкой),
            предложение ввести русское отображение понятия  (с оценкой),
            предложение ввести английское отображение понятия (с оценкой),
            предложение ввести русское отображение понятия (с оценкой),
            предложение ввести английское отображение понятия (с оценкой),
            вывод информации что тренировка данного понятия окончена
        """
        self.engTextWidget = urwid.AttrWrap(urwid.Text(self.eng_text, align=urwid.CENTER), "eng")
        self.rusTextWidget = urwid.AttrWrap(urwid.Text(self.rus_text, align=urwid.CENTER), "rus")
        arrowTextWidget = urwid.AttrWrap(urwid.Text("  -->  ", align=urwid.CENTER), "arrow")

        if self.mode_teacher == "start":
            box = urwid.LineBox(urwid.Text(
            "Внимательно вчитывайтесь в переводы.\nДля начала тренировки нажмите Enter. Удачи.", align=urwid.CENTER))
            padding = urwid.Padding(box, align=urwid.CENTER, width=(urwid.RELATIVE, 60))
            self.teacher = padding
        elif self.mode_teacher == "outruseng":
            columns = urwid.Columns([self.rusTextWidget, arrowTextWidget, self.engTextWidget])
            pile = urwid.Pile([self.one_line, columns, self.one_line])
            box = urwid.LineBox(pile, title="Запомните.")
            padding = urwid.Padding(box, align=urwid.CENTER, width=(urwid.RELATIVE, 60))
            self.teacher.original_widget = padding
        elif self.mode_teacher == "outengrus":
            columns = urwid.Columns([self.engTextWidget, arrowTextWidget, self.rusTextWidget,])
            pile = urwid.Pile([self.one_line, columns, self.one_line])
            box = urwid.LineBox(pile, title="Запомните.")
            padding = urwid.Padding(box, align=urwid.CENTER, width=(urwid.RELATIVE, 60))
            self.teacher.original_widget = padding
        elif self.mode_teacher == "inrus":
            pile = urwid.Pile([self.one_line, self.engTextWidget, self.one_line])
            box = urwid.LineBox(pile, title="Переведите на русский.")
            padding = urwid.Padding(box, align=urwid.CENTER, width=(urwid.RELATIVE, 60))
            self.teacher.original_widget = padding
        elif self.mode_teacher == "ineng":
            pile = urwid.Pile([self.one_line, self.rusTextWidget, self.one_line])
            box = urwid.LineBox(pile, title="Переведите на английский.")
            padding = urwid.Padding(box, align=urwid.CENTER, width=(urwid.RELATIVE, 60))
            self.teacher.original_widget = padding
        elif self.mode_teacher == "inrus1":
            pile = urwid.Pile([self.one_line, self.engTextWidget, self.one_line])
            box = urwid.LineBox(pile, title="Переведите на русский.")
            padding = urwid.Padding(box, align=urwid.CENTER, width=(urwid.RELATIVE, 60))
            self.teacher.original_widget = padding
        elif self.mode_teacher == "ineng1":
            pile = urwid.Pile([self.one_line, self.rusTextWidget, self.one_line])
            box = urwid.LineBox(pile, title="Переведите на английский.")
            padding = urwid.Padding(box, align=urwid.CENTER, width=(urwid.RELATIVE, 60))
            self.teacher.original_widget = padding
        elif self.mode_teacher == "inrus2":
            text = urwid.Text(("rus","На русском."), align=urwid.CENTER)
            pile = urwid.Pile([self.one_line, text, self.one_line])
            box = urwid.LineBox(pile, title="Последнее изучаемое слово:")
            padding = urwid.Padding(box, align=urwid.CENTER, width=(urwid.RELATIVE, 60))
            self.teacher.original_widget = padding
        elif self.mode_teacher == "ineng2":
            text = urwid.Text(("eng", "На английском."), align=urwid.CENTER)
            pile = urwid.Pile([self.one_line, text, self.one_line])
            box = urwid.LineBox(pile, title="Последнее изучаемое слово:")
            padding = urwid.Padding(box, align=urwid.CENTER, width=(urwid.RELATIVE, 60))
            self.teacher.original_widget = padding
        elif self.mode_teacher == "exit":
            text = urwid.Text("Вы выучили: ", align=urwid.CENTER)
            columns = urwid.Columns([self.rusTextWidget, arrowTextWidget, self.engTextWidget])
            columnsback = urwid.Columns([self.engTextWidget, arrowTextWidget, self.rusTextWidget,])
            pile = urwid.Pile([self.one_line, text, self.one_line, columns, columnsback, self.one_line, self.one_line])
            box = urwid.LineBox(pile, title="Тренировка понятия окончена.")
            padding = urwid.Padding(box, align=urwid.CENTER, width=(urwid.RELATIVE, 60))
            self.teacher.original_widget = padding



    def set_student(self):
        """
        Создает блок ученика.
        """
        self.student_edit_text = mywidgets.MyEdit(align=urwid.CENTER)
        pile = urwid.Pile([
            self.one_line,
            self.student_edit_text,
            self.one_line,
            ])
        box = urwid.LineBox(pile)
        padding = urwid.Padding(box, align=urwid.CENTER, width=(urwid.RELATIVE, 30))
        self.student = padding

