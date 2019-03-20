from widgets import *
from fields import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import webbrowser


class Link(Constraint):
    def __init__(self, items=None, **kwargs):
        super(Link, self).__init__(**kwargs)
        self.widget_1 = QToolButton()
        self.set_color("blue")
        self.widget_1.setText('go to original')


        self.widget_1.clicked.connect( self.open )

        self.master_layout.addWidget( self.widget_1)

    def open(self):
        for cons, v in self.root.constraints.items():
            if v['widget'].name == "popcorn":
                objw = self.root.objects[v['parent']]['widget']

                self.root.show_object_item_list( objw )
                ilw = self.root.item_lists[self.root.objects[v['parent']]['item_list']]['widget']
                ilw.ls[cons]['item_widget'].setSelected(True)
                print(v)
