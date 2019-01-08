
from widgets import *
from PySide.QtCore import *
from PySide.QtGui import * 

class Constraint(QWidget):
    def __init__(self, parent=None, **kwargs):
        super(Constraint, self).__init__(**kwargs)
        self.parent = parent
        self.id = str(uuid.uuid4())
        self.name = None
        self.meta_layout = QHBoxLayout()
        shrink_wrap(self.meta_layout, margin=2, spacing=5)
        self.ctrl_dots = QLabel(" ::")
        self.icon = Icon()

        self.meta_layout.addWidget(self.ctrl_dots)
        self.meta_layout.addWidget(self.icon)

        self.master_layout = QVBoxLayout()
        self.meta_layout.addLayout(self.master_layout)
        self.setLayout(self.meta_layout)
        shrink_wrap(self.master_layout, margin=2, spacing=2)
        self.title = EditLabel()
        self._name = None
        self.master_layout.addWidget(self.title, stretch=0)
        
        #self.mouseReleaseEvent = self._emit_id

        self.root = self.parent.parent


    def set_name(self, nm):
        self._name = nm
        self.title.set_text( self._name )

            
    
    def _emit_id(self, event):
        print(self.root.objects)
