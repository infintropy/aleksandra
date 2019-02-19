from widgets import *
from fields import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import * 

class TextBlock(Constraint):
    def __init__(self, **kwargs):
        super(TextBlock, self).__init__(**kwargs)
        
        self.widget_1 = QPlainTextEdit()
        self.set_color("teal")
        self.master_layout.addWidget(self.widget_1, stretch=0)
        self.master_layout.addStretch()
        self.widget_1.setMaximumHeight(100)