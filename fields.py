from PyQt5.QtCore import *
from PyQt5.QtWidgets import * 

from utils import shrink_wrap



class Field(QWidget):
    def __init__(self):
        super(Field, self).__init__()
        
        self._value = None
        self._widget = None
        self._master_layout = QVBoxLayout()
        shrink_wrap(self._master_layout)
        self.setLayout(self._master_layout)

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, val):
        if val:
            self._value = val
    
    def serialize(self):
        return None
        #return serialized dict of field
        #{'field_name'}

class ButtonChoice(Field):
    def __init__(self):
        super(Field, self).__init__()
        self._master_layout = QHBoxLayout()
        self._button_group = QButtonGroup()

        self._checked_css = "QAbstractButton::checked{background-color:rgba(30,50,100);}"
        self.setStyleSheet(self._checked_css)
        self.setLayout(self._master_layout)
        self._current_button = None
        self._button_group.buttonClicked.connect(self.radio_select)

    def add_buttons(self, button_list, span=False, adjust="left"):
        self._buttons = {}
        if adjust=="right":
            self._master_layout.addStretch()
        for b in button_list:
            self._buttons[b] = QToolButton()
            self._buttons[b].setText( b )
            self._buttons[b].setCheckable(True)
            self._master_layout.addWidget(self._buttons[b])
            self._button_group.addButton(self._buttons[b])
        if adjust=="left":
            self._master_layout.addStretch()

    def radio_select(self, button ):
        #placeholder
        print('clicking button %s' %button.text())
        self._current_button = button.text()

    def value(self):
        return self._current_button


class LineEdit(Field):
    def __init__(self):
        super(LineEdit, self).__init__()

        self._widget = QLineEdit()
        self._master_layout.addWidget(self._widget)

    def value(self):
        return self._widget.text()

class Dropdown(Field):
    def __init__(self, items=None):
        super(Dropdown, self).__init__()
        self._widget = QComboBox()
        self._master_layout.addWidget( self._widget )
        if items:
            self._widget.addItems(items)


    def add_items(self, items):
        self._widget.addItems(items)

    def value(self):
        return self._widget.currentText()

class Integer(Field):
    def __init__(self):
        super(Integer, self  ).__init__()
        self._widget = QSpinBox()
        self._master_layout.addWidget(self._widget)


class Boolean(Field):
    def __init__(self):
        super(Boolean, self  ).__init__()

        self._widget = QCheckBox()
        self._master_layout.addWidget(self._widget)

    def value(self):
        return self._widget.isChecked()

class Float(Field):
    def __init__(self):
        super(Float, self  ).__init__()
        self._widget = QSlider(Qt.Horizontal)
        self._master_layout.addWidget(self._widget)
