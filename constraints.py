import sys
from widgets import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import * 
import inspect





class List(Constraint):
    def __init__(self, **kwargs):
        super(List, self).__init__(**kwargs)

        self.ls = {}
        self.widget_1 = QListWidget()
        for i in ["Task%d" %d for d in range(4)]:
            self.add_item()

        self.master_layout.addWidget(self.widget_1)
        self.widget_1.setDragDropMode(QAbstractItemView.InternalMove)

    def add_item(self, name="Item"):
        o = ObjWidget(parent=self)
        self.ls[o.id] = {}
        self.ls[o.id]['widget'] = o
        self.ls[o.id]['item_widget'] = QListWidgetItem()
        self.ls[o.id]['item_widget'].setSizeHint(self.ls[o.id]["widget"].sizeHint())
        self.ls[o.id]['item_widget'].setSizeHint(QSize( 0, 35 ))
        self.widget_1.addItem(self.ls[o.id]['item_widget'])
        self.widget_1.setItemWidget( self.ls[o.id]['item_widget'], self.ls[o.id]['widget']) 
        self.root.add( o )


class Choice(Constraint):
    def __init__(self, items=None, **kwargs):
        super(Choice, self).__init__(**kwargs)
        self.widget_1 = QComboBox()
        if items:
            self.widget_1.addItems(items)
        else:
            self.widget_1.addItems(["Choice%d" %d for d in range(5)])
        self.master_layout.addWidget(self.widget_1)

class Checkbox(Constraint):
    def __init__(self, items=None, **kwargs):
        super(Checkbox, self).__init__(**kwargs)
        self.widget_1 = QCheckBox()
        self.master_layout.addWidget(self.widget_1)


class TextLine(Constraint):
    def __init__(self, **kwargs):
        super(TextLine, self).__init__(**kwargs)
        
        self.widget_1 = QLineEdit()
        self.master_layout.addWidget(self.widget_1, stretch=0)
        self.master_layout.addStretch()


class TextBlock(Constraint):
    def __init__(self, **kwargs):
        super(TextBlock, self).__init__(**kwargs)
        
        self.widget_1 = QPlainTextEdit()
        self.master_layout.addWidget(self.widget_1, stretch=0)
        self.master_layout.addStretch()
        self.widget_1.setMaximumHeight(100)

class Number(Constraint):
    def __init__(self, **kwargs):
        super(Number, self).__init__(**kwargs)
        self.id = str(uuid.uuid4())
        self.widget_1 = QSpinBox()
        self.master_layout.addWidget(self.widget_1)


class Price(Constraint):
    def __init__(self, **kwargs):
        super(Price, self).__init__(**kwargs)
        self.layout = QHBoxLayout()
        shrink_wrap(self.layout, margin=0, spacing=0)
        self.id = str(uuid.uuid4())
        self.symbol = QToolButton()
        self.symbol.setText("$")
        self.symbol.setFont(BUTTON_FONT)
        self.widget_1 = QSpinBox()
        self.layout.addWidget(self.symbol)
        self.layout.addWidget(self.widget_1)
        self.master_layout.addLayout(self.layout)


class CreationMenu(QMenu):
    def __init__(self):
        super(CreationMenu, self).__init__()
        self.constraints = constraint_widgets()
        self.act = {}

        for k in sorted(self.constraints.keys()):
            self.act[k] = QAction(self)
            self.addAction( self.act[k] )
            self.act[k].setText( k )


class ObjWidget(QWidget):

    def __init__(self, parent=None, name=None):
        super(ObjWidget, self).__init__()
        self.parent = parent
        self.id = str(uuid.uuid4())
        self.master_layout = QHBoxLayout()
        self.label = QLabel("Item")
        self.master_layout.addWidget( self.label )
        shrink_wrap(self.master_layout, margin=5, spacing=3)
        self.setLayout( self.master_layout )
        self.root = self.parent.parent.parent
        self.mouseReleaseEvent = self._emit_id
    
    def _emit_id(self, event):
        print(self.root.objects)