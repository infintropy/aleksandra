from widgets import *
from fields import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import * 

class MultipleChoice(Constraint):
    def __init__(self, name=None, **kwargs):
        super(MultipleChoice, self).__init__(**kwargs)

        self.widget_1 = QLabel('Whats the answer to this question?')
        self.answers = ButtonChoice()
        self.answers.add_buttons(['dog', 'cat', 'parrot'], adjust="right")
        self.ans = Dropdown(['trendle', 'derp'])
        self.num = Integer()
        self.boo = Boolean()
        self.float = Float()

        self.master_layout.addWidget( self.widget_1 )
        self.master_layout.addWidget( self.answers )
        self.master_layout.addWidget( self.ans )
        self.master_layout.addWidget( self.num )
        self.master_layout.addWidget( self.boo )
        self.master_layout.addWidget( self.float)