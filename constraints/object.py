from widgets import *
from fields import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


class Object(Constraint):
    def __init__(self, name=None, **kwargs):
        super(Object, self).__init__(**kwargs)

        self.mousePressEvent = self._emit_id

        self.obj = self.root.add_object(constraint=self, name=name, index=1)

        self.master_layout.addWidget(self.obj)
        self.title.setVisible(False)

    def _emit_id(self, e):
        self.root.show_object_item_list(self.obj, make=False)
        # print("(%s) level: %s" %(self.level, self.id ))
        self.mouseReleaseEvent(e)
