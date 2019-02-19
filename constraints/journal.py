from widgets import *
from fields import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import * 

class Journal(Constraint):
    def __init__(self, name='Journal', **kwargs):
        super(Journal, self).__init__(**kwargs)

        self.mousePressEvent = self._show_journals
        self.title.setVisible(False)
                
        self.obj = self.root.add_object(constraint=self, name=name, index=1)
        self._widget_1 = QPlainTextEdit()


        self.save = QPushButton("save")
        self.master_layout.addWidget(self.obj)
        self.master_layout.addWidget(self._widget_1)
        self.master_layout.addWidget(self.save)

        self.obj.make_list()

        self.save.clicked.connect( self.save_entry )

    def _show_journals(self, e):
        
        self.root.show_object_item_list(self.obj)
        #print("(%s) level: %s" %(self.level, self.id ))
        self.mouseReleaseEvent(e)

    def save_entry(self):
        ilid = self.root.objects[self.obj.id]["item_list"]
        il = self.root.item_lists[ilid]['widget']

        o = self.root.add_constraint( obj=self.obj, typ='TextBlock', level=self.obj.level )
        o.widget_1.setPlainText(self._widget_1.toPlainText())
        il.add_item(constraint=o)
