from widgets import *
from fields import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import * 

class List(Constraint):
    def __init__(self, **kwargs):
        super(List, self).__init__(**kwargs)
        self.set_color("green")
        self.ls = {}
        self.list_height = 0
        self.widget_1 = QListWidget()
        self.widget_1.setStyleSheet("border-radius:10px;")
        self.widget_1.setMaximumHeight(self.list_height)
        self.widget_1.setSizePolicy( QSizePolicy.Expanding, QSizePolicy.Minimum )


        self.master_layout.addWidget(self.widget_1)
        self.widget_1.setDragDropMode(QAbstractItemView.InternalMove)
        self.add_obj = QToolButton()
        self.add_obj.setText("+")
        self.title.label.master_layout.addWidget(self.add_obj)

        self.add_obj.clicked.connect( self.add_item )
        self.setSizePolicy( QSizePolicy.Expanding, QSizePolicy.Minimum )

    def add_item(self, name="Item"):

        o = self.root.add_object(constraint=self, name=name, index=1)
        
        self.ls[o.id] = {}
        self.ls[o.id]['widget'] = o
        self.ls[o.id]['item_widget'] = QListWidgetItem()
        self.ls[o.id]['item_widget'].setSizeHint(self.ls[o.id]["widget"].sizeHint())
        self.ls[o.id]['item_widget'].setSizeHint(QSize( 0, 35 ))
        self.widget_1.addItem(self.ls[o.id]['item_widget'])
        self.widget_1.setItemWidget( self.ls[o.id]['item_widget'], self.ls[o.id]['widget']) 

        oid = self.root.constraints[self.id]['parent']
        iliw = self.root.constraints[self.id]['item_widget']
        iliw.setSizeHint(QSize(0,self.height()+35))
        self.list_height+=35
        
        self.widget_1.setMaximumHeight(self.list_height+2)
        ilid = self.root.objects[oid]['item_list']
        self.root.item_lists[ilid]['widget'].update()
