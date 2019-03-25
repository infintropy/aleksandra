from widgets import *
from fields import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

"""
WARNING: The following code is intended only for the author. 
"""


#Day

class Midnight(Constraint):
    def __init__(self, items=None, **kwargs):
        super(Midnight, self).__init__(**kwargs)
        self.set_color( "red" )
        self.label = QLabel("12am|4am\nREST")
        self.master_layout.addWidget(self.label)

class Dawn(Constraint):
    def __init__(self, items=None, **kwargs):
        super(Dawn, self).__init__(**kwargs)
        self.set_color( "orange" )
        self.label = QLabel("4am|8am\nRISE")
        self.master_layout.addWidget(self.label)

class Morning(Constraint):
    def __init__(self, items=None, **kwargs):
        super(Morning, self).__init__(**kwargs)
        self.set_color( "yellow" )
        self.label = QLabel("8am|12pm\nFOCUS")
        self.master_layout.addWidget(self.label)

class MidDay(Constraint):
    def __init__(self, items=None, **kwargs):
        super(MidDay, self).__init__(**kwargs)
        self.set_color( "green" )
        self.label = QLabel("12pm|4pm\nDO")
        self.master_layout.addWidget(self.label)

class Dusk(Constraint):
    def __init__(self, items=None, **kwargs):
        super(Dusk, self).__init__(**kwargs)
        self.set_color( "blue" )
        self.label = QLabel("4pm|8pm\nREMEMBER")
        self.master_layout.addWidget(self.label)

class Evening(Constraint):
    def __init__(self, items=None, **kwargs):
        super(Evening, self).__init__(**kwargs)
        self.set_color( "pink" )
        self.label = QLabel("8pm|12am\nBE")
        self.master_layout.addWidget(self.label)