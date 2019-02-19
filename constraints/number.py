from widgets import *
from fields import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import * 

class Number(Constraint):
    def __init__(self, **kwargs):
        super(Number, self).__init__(**kwargs)
        self.set_color("yellow")
        self.id = str(uuid.uuid4())
        self.widget_1 = QSpinBox()
        self.master_layout.addWidget(self.widget_1)

    def validate(self):
        return False
