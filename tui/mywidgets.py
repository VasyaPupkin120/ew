"""
Набор видждетов с дополнительными свойствами.
"""
from pdb import lasti2lineno
import urwid
from urwid.widget import *

class MyEdit(urwid.Edit):
    """
    Переработанный класс поля ввода.
    """
    def __init__(self, *args, **kwargs):
        # Для контроля, какая клавиша нажата последней, задан атрибут last_press
        self.last_press = None
        # Для хранения введеного значеия после очистки строки ввода по нажатию на Enter
        self.save_edit_text = ""
        super().__init__(*args, **kwargs)


    def keypress(self, size, key):
        """
        Handle editing keystrokes, return others.
        Класс с некотороыми изменениями.

        >>> e, size = Edit(), (20,)
        >>> e.keypress(size, 'x')
        >>> e.keypress(size, 'left')
        >>> e.keypress(size, '1')
        >>> print(e.edit_text)
        1x
        >>> e.keypress(size, 'backspace')
        >>> e.keypress(size, 'end')
        >>> e.keypress(size, '2')
        >>> print(e.edit_text)
        x2
        >>> e.keypress(size, 'shift f1')
        'shift f1'
        """
        (maxcol,) = size


        p = self.edit_pos

        # запоминаем последнее нажатие
        self.last_press = key

        if self.valid_char(key):
            if (isinstance(key, text_type) and not
                    isinstance(self._caption, text_type)):
                # screen is sending us unicode input, must be using utf-8
                # encoding because that's all we support, so convert it
                # to bytes to match our caption's type
                key = key.encode('utf-8')
            self.insert_text(key)

        elif key == "esc":
            # чтобы отработал сигнал на нажатие, иначе он не генерируется
            self.insert_text("")

        elif key=="tab" and self.allow_tab:
            key = " "*(8-(self.edit_pos%8))
            self.insert_text(key)

        # elif key=="enter" and self.multiline:
        #     key = "\n"
        #     self.insert_text(key)
        elif key == "enter":
            # запоминается последнее содержимое, после чего оно очищается
            # чтобы не удалять последний введеный текст каждый раз при новом тренируемом слове
            self.save_edit_text = self.get_edit_text()
            self.set_edit_text("")

        elif self._command_map[key] == CURSOR_LEFT:
            if p==0: return key
            p = move_prev_char(self.edit_text,0,p)
            self.set_edit_pos(p)

        elif self._command_map[key] == CURSOR_RIGHT:
            if p >= len(self.edit_text): return key
            p = move_next_char(self.edit_text,p,len(self.edit_text))
            self.set_edit_pos(p)

        elif self._command_map[key] in (CURSOR_UP, CURSOR_DOWN):
            self.highlight = None

            x,y = self.get_cursor_coords((maxcol,))
            pref_col = self.get_pref_col((maxcol,))
            assert pref_col is not None
            #if pref_col is None:
            #    pref_col = x

            if self._command_map[key] == CURSOR_UP: y -= 1
            else: y += 1

            if not self.move_cursor_to_coords((maxcol,),pref_col,y):
                return key

        elif key=="backspace":
            self.pref_col_maxcol = None, None
            if not self._delete_highlighted():
                if p == 0: return key
                p = move_prev_char(self.edit_text,0,p)
                self.set_edit_text( self.edit_text[:p] +
                    self.edit_text[self.edit_pos:] )
                self.set_edit_pos( p )

        elif key=="delete":
            self.pref_col_maxcol = None, None
            if not self._delete_highlighted():
                if p >= len(self.edit_text):
                    return key
                p = move_next_char(self.edit_text,p,len(self.edit_text))
                self.set_edit_text( self.edit_text[:self.edit_pos] +
                    self.edit_text[p:] )

        elif self._command_map[key] in (CURSOR_MAX_LEFT, CURSOR_MAX_RIGHT):
            self.highlight = None
            self.pref_col_maxcol = None, None

            x,y = self.get_cursor_coords((maxcol,))

            if self._command_map[key] == CURSOR_MAX_LEFT:
                self.move_cursor_to_coords((maxcol,), LEFT, y)
            else:
                self.move_cursor_to_coords((maxcol,), RIGHT, y)
            return

        else:
            # key wasn't handled
            return key
