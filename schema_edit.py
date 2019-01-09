from __future__ import print_function
import sys
import inspect

from functools import partial
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import uuid
import theme
import six
from constraints import *
from widgets import *




''' 
Can be viewed as objects with attributes. 
Can be viewed as a dependency tree

Users will interact with a constraint tree:
    Contraint = Frame Range
    Contraint_features = <start, 
                          end>
    Constraint_img = "Film time.png"
    Constraint_valid



Shot ___________|
________________|
Frame Range     | 
[             ] |
________________|
ConstraintSet   |
[             ] |






'''





def constraint_widgets():
    constraints = {}
    for name, obj in inspect.getmembers(sys.modules[__name__]):
        if inspect.isclass(obj):
            if issubclass( obj, Constraint ):
                if obj is not Constraint:
                    constraints[obj.__name__] = obj
    return constraints




#########
### MENU
#########
class CreationMenu(QMenu):
    def __init__(self):
        super(CreationMenu, self).__init__()
        self.constraints = constraint_widgets()
        self.act = {}

        for k in sorted(self.constraints.keys()):
            self.act[k] = QAction(self)
            self.addAction( self.act[k] )
            self.act[k].setText( k )


class ItemList(QWidget):
    def __init__(self, parent=None):

        super(ItemList, self).__init__()
        self.level = 1000
        self.master_layout = QVBoxLayout()
        
        self.id = str(uuid.uuid4())

        shrink_wrap(self.master_layout)
        self.setLayout( self.master_layout )
        self.lw = QListWidget()
        self.parent = parent
        self.root = self.parent
        self.ls = {}
        self.setFixedWidth(500)


        self.title = EditLabel()
        self.title_font = QFont()
        self.title_font.setPointSize(15)
        self.title.label.label.setFont(self.title_font)
        self.title.label.label.setMinimumHeight(30)
        self.title.label.label.setMaximumHeight(30)
        self.title.setMinimumHeight(30)

        self.master_layout.addWidget( self.title )
        self.master_layout.addWidget( self.lw)
        self.lw.setDragDropMode(QAbstractItemView.InternalMove)
        self.lw.setResizeMode(QListView.Adjust)

        self.cmd = {"object": ObjWidget}
        for c, w in six.iteritems(constraint_widgets()):
            self.cmd[c] = w
            self.add_item( c )

        
    def add_item(self,  typ=None):
        name="Item"
        print(typ)
        if typ:
            if typ in [k for k,v in six.iteritems(self.cmd)]:
                o = self.cmd[typ](parent=self)
                o.set_name(name)

                self.root.add( o )
                self.ls[o.id] = {}
                self.ls[o.id]['widget'] = o
                self.ls[o.id]['item_widget'] = QListWidgetItem()

                self.ls[o.id]['item_widget'].setSizeHint(self.ls[o.id]["widget"].sizeHint())

                self.lw.addItem(self.ls[o.id]['item_widget'])
                self.lw.setItemWidget( self.ls[o.id]['item_widget'], self.ls[o.id]['widget'])


        

class Window(QMainWindow):
    def __init__(self):
        super(Window, self).__init__()


        """
        STORE: for (x) object:
        key=id +++++++++++++++
        ++++++++++++++++++++++
        dependency_list = ItemList id
        parent_constraint = Constraint id


        """

        self.objects = {}
        self.item_lists = {}
        self.constraints = {}

        


        self.main = QWidget()
        self.setCentralWidget(self.main)
        self.logo = QLabel("aleksandra")
        self.logo_font = QFont()
        self.logo_font.setPointSize(13) 
        self.logo_font.setFamily("Courier")
        self.logo.setFont(self.logo_font)

        self.setWindowTitle('aleksandra')

        self.stacker1 = QStackedWidget()
        self.stack_level = {1: self.stacker1}


        self.file_menu = QMenu(self.menuBar())
        self.file_menu.setTitle("File")
        self.act_open = QAction(self.file_menu)
        self.act_open.setText("Open")
        self.act_open.setShortcut("Ctrl+O")
        self.file_menu.addAction(self.act_open)
        self.setUnifiedTitleAndToolBarOnMac(True)

        self.menuBar().addMenu( self.file_menu )


        self.make = QToolButton()
        self.make.setText("+")

        self.setMinimumWidth(700)
        self.setMinimumHeight(500)

        self.master_layout = QVBoxLayout()
        self.il = ItemList(self)
        #self.add( self.il )

        self.add_menu = CreationMenu()
        for a in list(self.add_menu.act.keys()):
            self.add_menu.act[a].triggered.connect(partial(self.il.add_item, a))
            self.add_menu.act[a].triggered.connect(partial(print, a))



        self.scroll = QScrollArea(alignment=Qt.Horizontal)
        self.mil_col_widget = QWidget()

        self.mil_col = QHBoxLayout(self.mil_col_widget)
        shrink_wrap(self.mil_col)
        
        self.scroll.setWidget(self.mil_col_widget)
        self.scroll.setWidgetResizable(True)
        self.mil_col.addWidget(self.il)
        self.mil_col.addStretch()

        self.make.setMenu( self.add_menu )
        self.make.setPopupMode(QToolButton.InstantPopup)

 
        self.master_layout.addWidget( self.logo )
        self.master_layout.addWidget( self.make )
        self.master_layout.addWidget( self.scroll)
        self.main.setLayout( self.master_layout )

    def add(self, item):

        if issubclass(type(item), Constraint):
            self.constraints[item.id] = {}
            self.constraints[item.id]['widget'] = item
            self.constraints[item.id]['parent'] = item.parent
            return item

        elif issubclass(type(item), ItemList):
            self.item_lists[item.id] = {}
            self.item_lists[item.id]['widget'] = item
            self.item_lists[item.id]['column'] = 1000
            return it

        elif isinstance(type(item), ObjWidget):
            self.objects[item.id] = {}
            self.objects[item.id]['widget'] = item
            self.objects[item.id]['constr'] = item.parent
            print('obj added!')
            return item




    def obj_focus(self, obj):
        pass

    def add_list_to_col(self):
        ind = len(self.stack_level.keys())+index
        self.stack_level[ind] = ItemList(self)
        self.mil_col.insertWidget( len(self.stack_level.keys())-1, self.stack_level[ind] )
   

    def add_list(self, index=1):

        ind = len(self.stack_level.keys())+index
        self.stack_level[ind] = ItemList(self)
        self.add( self.stack_level[ind] )
        self.mil_col.insertWidget( len(self.stack_level.keys())-1, self.stack_level[ind] )
   
    def update(self):
        self.il.add_item()


if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = Window()

    app.setStyle("Fusion")
    theme.dark(app)

    window.show()
    app.exec_()

"""
Window > List Manager > List


window.list[id].child()        
"""
