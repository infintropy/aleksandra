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

import qdarkstyle







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
    def __init__(self, parent=None, level=9000):

        super(ItemList, self).__init__()

        self.level = level
        self.master_layout = QVBoxLayout()
        self.id = str(uuid.uuid4())
        self.parent = parent
        shrink_wrap(self.master_layout)
        self.setLayout( self.master_layout )
        self.lw = QListWidget()
        self.root = self.parent
        self.ls = {}
        #self.setFixedWidth(500)
        self.setMinimumWidth(350)
        self.setMaximumWidth(500)
        print('init of imtemlist. level: %d' %self.level)
        self.setSizePolicy( QSizePolicy.Minimum, QSizePolicy.Expanding )
        self.title = EditLabel()
        self.title_font = QFont()
        self.title_font.setPointSize(24)
        self.title.label.label.setFont(self.title_font)
        self.title.label.label.setMinimumHeight(40)
        self.title.label.label.setMaximumHeight(40)
        self.title.setMinimumHeight(40)

        self.title.set_text( str(self.level) )

        self.master_layout.addWidget( self.title )
        self.master_layout.addWidget( self.lw)
        self.lw.setDragDropMode(QAbstractItemView.InternalMove)
        self.lw.setResizeMode(QListView.Adjust)

        self.lw.itemDoubleClicked.connect( self.dc )

        objlink = self.get_object_link()
        for c, w in six.iteritems(constraint_widgets()):
            
            if parent:
                if c=="List22":
                    print('lower init of imtemlist. level: %d' %self.level)
                    o = self.root.add_constraint( obj=objlink, typ=c, level=self.level )
                    self.add_item(constraint=o)

        self.title.edited.connect(self._update_upstream_title)

    #reimplementations of QWidget base class and beyond.
    def contextMenuEvent(self, event):
        menu = CreationMenu()
        action = menu.exec_(self.mapToGlobal(event.pos()))
        if action:
            objlink = self.get_object_link()
            o = self.root.add_constraint( obj=objlink, typ=action.text(), level=self.level )
            self.add_item(constraint=o)


    def _update_upstream_title(self, title):
        objlink = self.get_object_link()
        objlink.label.set_text( self.title.text() )



    def add_item(self,  constraint=None):
        cons = constraint

        self.ls[cons.id] = {}
        self.ls[cons.id]['widget'] = cons
        self.ls[cons.id]['item_widget'] = QListWidgetItem()
        
        self.ls[cons.id]['item_widget'].setSizeHint(self.ls[cons.id]["widget"].sizeHint())

        self.lw.addItem(self.ls[cons.id]['item_widget'])
        self.lw.setItemWidget( self.ls[cons.id]['item_widget'], self.ls[cons.id]['widget'])

    def dc(self):
        print( "item double clicked!" )

    def set_parent(self, parent=None):
        if parent:
            self.parent=parent
            self.root = self.parent

    def get_object_link(self):
        try:
            objlinkid = self.root.item_lists[self.id]['objlink']
            objlink = self.root.objects[objlinkid]['widget']
            return objlink
        except:
            return None


    def add_examples(self):
        try:
            objlinkid = self.root.item_lists[self.id]['objlink']
            objlink = self.root.objects[objlinkid]['widget']
        except:
            objlink = self.root.root_obj
        for c, w in six.iteritems(constraint_widgets()):
            o = self.root.add_constraint( obj=objlink, typ=c )


        

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


        self._col_start = 9000
        self.metacol = {}


        self.main = QWidget()
        self.setCentralWidget(self.main)
        self.logo = QLabel("aleksandra")
        self.logo_font = QFont()
        self.logo_font.setPointSize(13) 
        self.logo_font.setFamily("Courier")
        self.logo.setFont(self.logo_font)

        self.setWindowTitle('aleksandra')


        self.root_item_list = ItemList()
        self.root_list = List()
        self.root_obj = ObjWidget()

        self.add_object(obj=self.root_obj, constraint=self.root_list)
        self.add_constraint(constraint=self.root_list, obj=None)


        self.file_menu = QMenu(self.menuBar())
        self.file_menu.setTitle("File")
        self.act_open = QAction(self.file_menu) 
        self.act_open.setText("Open")
        self.act_open.setShortcut("Ctrl+O")
        self.file_menu.addAction(self.act_open)
        self.setUnifiedTitleAndToolBarOnMac(True)

        self.menuBar().addMenu( self.file_menu )
        self.stack_level = {}





        self.setMinimumWidth(700)
        self.setMinimumHeight(500)

        self.master_layout = QVBoxLayout()
        #self.il = ItemList(self)

    


        self.add_menu = CreationMenu()
        for a in list(self.add_menu.act.keys()):

            self.add_menu.act[a].triggered.connect(partial(self.add_constraint, None, None))
            pass



        self.scroll = QScrollArea(alignment=Qt.Horizontal)
        self.mil_col_widget = QWidget()
        self.mil_col_layout = QGridLayout()

        self.miller_layout = QHBoxLayout()
        shrink_wrap(self.miller_layout)

        self.miller_spacer = QSpacerItem(1  , 1, QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.miller_layout.addLayout(self.mil_col_layout)
        self.miller_layout.addItem( self.miller_spacer )
        
        self.mil_col_widget.setLayout(self.miller_layout)


        self.mil_col_widget.setSizePolicy( QSizePolicy.Minimum, QSizePolicy.Expanding )

        #shrink_wrap(self.mil_col)
        #self.mil_col.setAlignment(Qt.AlignLeft)
        self.scroll.setWidget(self.mil_col_widget)
        self.scroll.setWidgetResizable(True)
        




 
        self.master_layout.addWidget( self.logo )
        self.master_layout.addWidget( self.scroll)
        self.main.setLayout( self.master_layout )


        print(self.objects)
        print(self.constraints)
        print(self.item_lists)



        self.add_item_list(obj=self.root_obj)
        #self.add_constraint(obj=self.root_obj)

        #self.end_spacer = QWidget()
        #self.mil_col_widget.addWidget(self.end_spacer)
        #self.mil_col_widget.setStretchFactor(1, 1)

        
        #self.mil_col_widget.addWidget(None)


    def get_object(self, id=None):                                                      
        pass
    
    def get_constraint(self, id=None):
        pass

    def get_item_list(self, id=None):
        pass



    def show_object_item_list(self, obj):

        if type(obj)==str:
            odict = self.objects[obj]
        else:
            odict = self.objects[obj.id]
        o = odict['widget']

        level = obj.level
        if odict["item_list"]:
            for l in list(self.metacol.keys()):
                if l <= level:
                    self.metacol[l].setVisible(True)
                else:
                    self.metacol[l].setVisible(False)
            #print(self.metacol[level].count())
            self.metacol[level].setCurrentWidget( self.item_lists[ self.objects[obj.id]['item_list']]['widget'] )
        else:
            self.add_item_list(obj=o)


 


    def add_item_list(self, item_list=None, obj=None, index=0):
        '''
        This will be where you manage your item scroll lists in in-place
        dimension, as well as their horizontal dimension. 

        parent= object

        '''
        

        level = obj.level

        
        if not item_list:
            item_list = ItemList(parent=self, level=level)
        self.item_lists[item_list.id] = {}
        self.item_lists[item_list.id]['widget'] = item_list
        self.item_lists[item_list.id]['objlink'] = obj.id
        self.objects[obj.id]["item_list"] = item_list.id
        #self.add_list(item_list)

        if not self.metacol.get(level):
            print("MAKING NEW STACKER %d" %level)
            self.metacol[level] = QStackedWidget()
            stack = self.metacol[level]
        
        self.metacol[level].addWidget( self.item_lists[item_list.id]['widget'] )
        self.metacol[level].setCurrentWidget(  self.item_lists[item_list.id]['widget'] )
        self.mil_col_layout.addWidget(  self.metacol[level], 0, level-9000)

        for l in list(self.metacol.keys()):
            if l <= level:
                self.metacol[l].setVisible(True)
            else:
                self.metacol[l].setVisible(False)


        return item_list


    def add_object(self, obj=None, constraint=None, name="Item", index=0):
        """
        Method for adding an item to a provided List constraint or adding it to the root list. 
        """
        cons = constraint
        if not constraint:
            cons = self.root_list
        if not obj:
            obj = ObjWidget(parent=self, level=cons.level+index)
        else:
            obj.level = (cons.level + index)
            
        self.objects[obj.id] = {}
        self.objects[obj.id]['widget'] = obj
        self.objects[obj.id]['parent'] = cons.id
        self.objects[obj.id]['item_list'] = None
        self.objects[obj.id]['level'] = obj.level
        return obj


        
    def add_constraint(self,  constraint=None, obj=None,  typ="List", level=9000):
        """
        Adding a constraint to an object 
        """

        cons = constraint
        if not obj:
            obj = self.root_obj
        if not constraint:
            if type(typ)!=str:
                typ = typ[1]

            cons = self.cmd[typ](parent=self, level=level)


        self.constraints[cons.id] = {}
        self.constraints[cons.id]['widget'] = cons
        self.constraints[cons.id]['parent'] = obj.id
        
        item_list = self.objects[obj.id]['item_list']
        return cons


    def object_focus(self, id): 
        print('focusing on object %s' %id)

    def obj_focus(self, obj):
        pass

    def add_list_to_col(self, item_list=None):
        ind = len(self.stack_level.keys())+index
        if not item_list:
            item_list = ItemList(self)
        self.stack_level[ind] = item_list
        self.mil_col.insertWidget( len(self.stack_level.keys())-1, self.stack_level[ind] )
   

    def add_list(self, item_list=None, index=0):

        ind = len(self.stack_level.keys())+index
        if not item_list:
            item_list = ItemList(self)
        self.stack_level[ind] = item_list
        self.mil_col.addWidget( self.stack_level[ind] )
   
    def update(self):
        pass


if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = Window()

    app.setStyle("Fusion")


    # setup stylesheet
    #app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    theme.dark(app)


    window.show()

    app.exec_()

"""
Window > List Manager > List


window.list[id].child()        
"""
