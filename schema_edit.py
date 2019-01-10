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
            o = self.root.add_constraint( obj=self.root.root_obj, typ=c )
            self.add_item(constraint=o)
        
    def add_item(self,  constraint=None):
        cons = constraint

        self.ls[cons.id] = {}
        self.ls[cons.id]['widget'] = cons
        self.ls[cons.id]['item_widget'] = QListWidgetItem()

        self.ls[cons.id]['item_widget'].setSizeHint(self.ls[cons.id]["widget"].sizeHint())

        self.lw.addItem(self.ls[cons.id]['item_widget'])
        self.lw.setItemWidget( self.ls[cons.id]['item_widget'], self.ls[cons.id]['widget'])


        

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

        self.cmd = {}
        for c, w in six.iteritems(constraint_widgets()):
            self.cmd[c] = w
    


        self.context_object = None


        self._col_start = 1000
        self.metacol = {self._col_start: QStackedWidget()}


        self.main = QWidget()
        self.setCentralWidget(self.main)
        self.logo = QLabel("aleksandra")
        self.logo_font = QFont()
        self.logo_font.setPointSize(13) 
        self.logo_font.setFamily("Courier")
        self.logo.setFont(self.logo_font)

        self.setWindowTitle('aleksandra')


        self.root_item_list = ItemList(parent=None)
        self.root_list = List(parent=None)
        self.root_obj = ObjWidget(parent=self.root_list)
        

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

        self.add_object(obj=self.root_obj, name='root' )
        self.objects[self.root_obj.id]['item_list'] = self.root_item_list.id

        self.add_menu = CreationMenu()
        for a in list(self.add_menu.act.keys()):
            pass
            #self.add_menu.act[a].triggered.connect(partial(self.il.add_item, a))




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

    def get_object(self, id=None):
        pass
    
    def get_constraint(self, id=None):
        pass

    def get_item_list(self, id=None):
        pass


    def add_object(self, obj=None, constraint=None, name="Item"):
        """
        Method for adding an item to a provided List constraint or adding it to the root list. 
        """
        cons = constraint
        if not constraint:
            cons = self.root_list
        if not obj:
            obj = ObjWidget(parent=cons)
        else:
            self.objects[obj.id] = {}
            self.objects[obj.id]['widget'] = obj
            self.objects[obj.id]['parent'] = cons.id
            self.objects[obj.id]['item_list'] = None
            print('obj added!')
        return obj
        
    def add_constraint(self,  obj=None, constraint=None, typ="List"):
        """
        Adding a constraint to an object 
        """
        cons = constraint
        if not obj:
            obj = self.root_obj
        if not constraint:
            cons = self.cmd[typ](parent=obj)
        else:
            self.constraints[cons.id] = {}
            self.constraints[cons.id]['widget'] = cons
            self.constraints[cons.id]['parent'] = obj.id
            print('constraint added!')
        return cons


    def add(self, item):
        pass
        if type(item)==type(""):
            print (item)
            cmd = item
            item = None
            constraints = list(self.add_menu.act.keys())

            if cmd in constraints:
                item = self.cmd[cmd]()
                print("making a constraint")
            elif cmd == "ObjWidget":
                print("making an object")
            elif cmd== "ItemList":
                print("making an ItemList")

        if item:
            par = item.parent.__class__.__name__
            if par=="Window":
                self.item_lists[item.id] = {}
                self.item_lists[item.id]['widget'] = item
                self.item_lists[item.id]['column'] = 1000
                print("Item List added!")
                return item
            elif par=="ItemList":
                self.constraints[item.id] = {}
                self.constraints[item.id]['widget'] = item
                self.constraints[item.id]['parent'] = item.parent
                print('constraint added!')
                return item
            elif par=="List":
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
        pass


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
