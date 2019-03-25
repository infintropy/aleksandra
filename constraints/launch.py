from widgets import *
from fields import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import * 
import webbrowser
from sdc import Sidecar

class LaunchURL(Constraint):
    def __init__(self, items=None, **kwargs):
        super(LaunchURL, self).__init__(**kwargs)
        self.widget_1 = QToolButton()
        self.set_color("orange")
        self.widget_1.setText('launch app')
        self.url = QLineEdit()
        self.url.setText("http://google.com")
        self.master_layout.addWidget(self.widget_1)
        self.master_layout.addWidget(self.url)

        self.widget_1.clicked.connect( self.open )

    def open(self):

        webbrowser.open(self.url.text(), new=2)


class LaunchCommand(Constraint):
    def __init__(self, items=None, **kwargs):
        super(LaunchCommand, self).__init__(**kwargs)
        self.widget_1 = QToolButton()
        self.lang = Dropdown(['python', 'ruby'])
        self.set_color("orange")
        self.widget_1.setText('launch app')
        self.url = QLineEdit()
        self.url.setText("http://google.com")

        self.master_layout.addWidget(self.widget_1)
        self.master_layout.addWidget(self.url)
        self.master_layout.addWidget(self.lang)
        self.master_layout.addWidget(self.sdc)

        self.widget_1.clicked.connect( self.open )

    def open(self):

        webbrowser.open(self.url.text(), new=2)