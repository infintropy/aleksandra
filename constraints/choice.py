from widgets import *
from fields import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import * 


class Choice(Constraint):
    def __init__(self, items=None, **kwargs):
        super(Choice, self).__init__(**kwargs)
        self.widget_1 = Dropdown()
        self.set_color("blue")
        if items:
            self.widget_1.add_items(items)
        else:
            self.widget_1.add_items(["Choice%d" %d for d in range(5)])
        self.master_layout.addWidget(self.widget_1)

        self.widget_1._widget.currentIndexChanged.connect( self.reg )

        self.fields.append( self.widget_1 )

    def reg(self):
        print (self.save())
