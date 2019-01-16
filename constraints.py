import sys
from widgets import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import * 
import inspect
import aleksa




class List(Constraint):
    def __init__(self, **kwargs):
        super(List, self).__init__(**kwargs)
        self.set_color("green")
        self.ls = {}
        self.widget_1 = QListWidget()
        if kwargs.get("parent"):
            for i in ["Task%d" %d for d in range(4)]:
                self.add_item()

        self.master_layout.addWidget(self.widget_1)
        self.widget_1.setDragDropMode(QAbstractItemView.InternalMove)

    def add_item(self, name="Item"):

        o = self.root.add_object(constraint=self, name=name, index=1)
        
        self.ls[o.id] = {}
        self.ls[o.id]['widget'] = o
        self.ls[o.id]['item_widget'] = QListWidgetItem()
        self.ls[o.id]['item_widget'].setSizeHint(self.ls[o.id]["widget"].sizeHint())
        self.ls[o.id]['item_widget'].setSizeHint(QSize( 0, 35 ))
        self.widget_1.addItem(self.ls[o.id]['item_widget'])
        self.widget_1.setItemWidget( self.ls[o.id]['item_widget'], self.ls[o.id]['widget']) 




class Choice(Constraint):
    def __init__(self, items=None, **kwargs):
        super(Choice, self).__init__(**kwargs)
        self.widget_1 = QComboBox()
        self.set_color("blue")
        if items:
            self.widget_1.addItems(items)
        else:
            self.widget_1.addItems(["Choice%d" %d for d in range(5)])
        self.master_layout.addWidget(self.widget_1)

class Checkbox(Constraint):
    def __init__(self, items=None, **kwargs):
        super(Checkbox, self).__init__(**kwargs)
        self.widget_1 = QCheckBox()
        self.set_color("olive")
        self.master_layout.addWidget(self.widget_1)


class TextLine(Constraint):
    def __init__(self, **kwargs):
        super(TextLine, self).__init__(**kwargs)
        self.set_color("red")
        self.widget_1 = QLineEdit()
        self.master_layout.addWidget(self.widget_1, stretch=0)
        self.master_layout.addStretch()


class TextBlock(Constraint):
    def __init__(self, **kwargs):
        super(TextBlock, self).__init__(**kwargs)
        
        self.widget_1 = QPlainTextEdit()
        self.set_color("teal")
        self.master_layout.addWidget(self.widget_1, stretch=0)
        self.master_layout.addStretch()
        self.widget_1.setMaximumHeight(100)

class Number(Constraint):
    def __init__(self, **kwargs):
        super(Number, self).__init__(**kwargs)
        self.set_color("yellow")
        self.id = str(uuid.uuid4())
        self.widget_1 = QSpinBox()
        self.master_layout.addWidget(self.widget_1)


class Price(Constraint):
    def __init__(self, **kwargs):
        super(Price, self).__init__(**kwargs)
        self.layout = QHBoxLayout()
        self.set_color("orange")
        shrink_wrap(self.layout, margin=0, spacing=0)
        self.id = str(uuid.uuid4())
        self.symbol = QToolButton()
        self.symbol.setText("$")
        self.symbol.setFont(BUTTON_FONT)
        self.widget_1 = QSpinBox()
        self.layout.addWidget(self.symbol)
        self.layout.addWidget(self.widget_1)
        self.master_layout.addLayout(self.layout)

class File(Constraint):
    def __init__(self, **kwargs):
        super(File, self).__init__(**kwargs)

        self.layout = QHBoxLayout()
        self.file_path = QLineEdit()
        self.file_path.setPlaceholderText("/path/to/file.txt")
        self.master_layout.addWidget(self.file_path)



class ScreenLocation(Constraint):
    def __init__(self, **kwargs):
        super(ScreenLocation, self).__init__(**kwargs)
        """
        USL     UC      USR
        CSL     C       CSR
        LSL     LC      LCR
        """
        self.ak = aleksa.ScreenLocation()
        self.depth_options = self.ak._z_possibilities

        self.buttons = {"USL" : (1,1),
                        "UC"  : (1,2),
                        "USR" : (1,3),
                        "CSL" : (2,1),
                        "C"   : (2,2),
                        "CSR" : (2,3),
                        "LSL" : (3,1),
                        "LC"  : (3,2),
                        "LCR" : (3,3)
                        }
        self.layout = QHBoxLayout()
        shrink_wrap(self.layout)
        self.button_layout = QGridLayout()
        for k,v in self.buttons.items():
            but = QToolButton()
            but.setFixedWidth(30)
            but.setFixedHeight(30)
            but.setText(k)
            but.setCheckable(True)
            self.button_layout.addWidget( but, v[0], v[1] )

        self._z_combo = QComboBox()
        for c,d in enumerate(["BG", "MG", "FG"]):
            self._z_combo.addItems([i for i in self.depth_options if d in i])
        self._z_combo.insertSeparator(5)
        self._z_combo.insertSeparator(11)
        self.layout.addLayout( self.button_layout )
        self.layout.addWidget( self._z_combo)
        self.master_layout.addLayout(self.layout)

