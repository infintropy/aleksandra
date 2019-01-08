from __future__ import print_function
import sys
import inspect

from functools import partial
from PySide2.QtCore import *
from PySide2.QtWidgets import *
from PySide2.QtGui import *
import uuid
import theme
import aleksa


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

#GLOBAL VARS

BUTTON_FONT = QFont()

BUTTON_FONT.setFamily('Helvetica')
BUTTON_FONT.setPointSize(13)







def constraint_widgets():
    constraints = {}
    for name, obj in inspect.getmembers(sys.modules[__name__]):
        if inspect.isclass(obj):
            if issubclass( obj, Constraint ):
                if obj is not Constraint:
                    constraints[obj.__name__] = obj
    return constraints

#function to set content margins easily for layouts. 
def shrink_wrap(layout, margin=2, spacing=2):
    layout.setContentsMargins(margin,margin,margin,margin)
    layout.setSpacing(spacing)


class NameBadge(QWidget):
    def __init__(self, label=None):
        super(NameBadge, self).__init__()
        self.label = QToolButton()
        self.label.setFont( BUTTON_FONT )
        self.label.setAutoRaise(True)

        self.fav = QToolButton(  )
        self.fav.setText( "<3" )
        self.fav.setCheckable(True)

        self.req = QToolButton()
        self.req.setText("+")
        
        self.req.setCheckable(True)

        self.menu = QMenu()
        self.act_fav = QAction(self.menu)
        self.act_fav.setText("make favorite")

        self.menu.addAction(self.act_fav)
        self.label.setMenu( self.menu )



        self.label.setText("button")
        self.master_layout = QHBoxLayout()
        self.master_layout.addWidget(self.label)
        self.master_layout.addStretch()

        self.master_layout.addWidget( self.req)
        self.master_layout.addWidget( self.fav )

        self.setLayout(self.master_layout)
        self.label.setMinimumHeight(20)
        self.label.setMaximumHeight(20)

        shrink_wrap(self.master_layout)

        self.favorite = QToolButton()
        self.favorite.setText("*")


    def add_favorite(self):
        pass






class EditLabel(QStackedWidget):
    def __init__(self, label=None):
        super(EditLabel, self).__init__()
        self.label = NameBadge()
  
        self.edit = QLineEdit() 

        self.setMaximumHeight(20)


        self.addWidget( self.label)
        self.addWidget( self.edit )

        self.label.label.setText("button")

        self.label.label.clicked.connect(self.edit_text)
        self.edit.editingFinished.connect( self.commit_text )

    def edit_text(self):
        self.setCurrentWidget( self.edit )

    def commit_text(self):
        self.setCurrentWidget( self.label )
        self.set_text( self.edit.text() )

    def set_text(self, txt):
        self.label.label.setText(txt)
        self.edit.setText(txt)

class Constraint(QWidget):
    def __init__(self, **kwargs):
        super(Constraint, self).__init__(**kwargs)
        self.id = str(uuid.uuid4())
        self.name = None
        self.meta_layout = QHBoxLayout()
        shrink_wrap(self.meta_layout, margin=2, spacing=5)
        self.ctrl_dots = QLabel(" ::")
        self.meta_layout.addWidget(self.ctrl_dots)

        self.master_layout = QVBoxLayout()
        self.meta_layout.addLayout(self.master_layout)
        self.setLayout(self.meta_layout)
        shrink_wrap(self.master_layout, margin=5, spacing=5)
        self.title = EditLabel()
        self._name = None
        self.master_layout.addWidget(self.title, stretch=0)



    def set_name(self, nm):
        self._name = nm
        self.title.set_text( self._name )

class List(Constraint):
    def __init__(self, **kwargs):
        super(List, self).__init__()
        self.widget_1 = QListWidget()
        for i in ["Task%d" %d for d in range(4)]:
            it = QListWidgetItem(i)
            it.setSizeHint(QSize(0, 35))
            self.widget_1.addItem(it)
        self.master_layout.addWidget(self.widget_1)
        self.widget_1.setDragDropMode(QAbstractItemView.InternalMove)

class Choice(Constraint):
    def __init__(self, items=None, **kwargs):
        super(Choice, self).__init__()
        self.widget_1 = QComboBox()
        if items:
            self.widget_1.addItems(items)
        else:
            self.widget_1.addItems(["Choice%d" %d for d in range(5)])
        self.master_layout.addWidget(self.widget_1)

class Checkbox(Constraint):
    def __init__(self, items=None, **kwargs):
        super(Checkbox, self).__init__()
        self.widget_1 = QCheckBox()
        self.master_layout.addWidget(self.widget_1)


class String(Constraint):
    def __init__(self, **kwargs):
        super(String, self).__init__(**kwargs)
        
        self.widget_1 = QLineEdit()
        self.master_layout.addWidget(self.widget_1, stretch=0)
        self.master_layout.addStretch()



class Number(Constraint):
    def __init__(self, **kwargs):
        super(Number, self).__init__(**kwargs)
        self.id = str(uuid.uuid4())
        self.widget_1 = QSpinBox()
        self.master_layout.addWidget(self.widget_1)


class Price(Constraint):
    def __init__(self, **kwargs):
        super(Price, self).__init__(**kwargs)
        self.layout = QHBoxLayout()
        shrink_wrap(self.layout, margin=0, spacing=0)
        self.id = str(uuid.uuid4())
        self.symbol = QToolButton()
        self.symbol.setText("$")
        self.symbol.setFont(BUTTON_FONT)
        self.widget_1 = QSpinBox()
        self.layout.addWidget(self.symbol)
        self.layout.addWidget(self.widget_1)
        self.master_layout.addLayout(self.layout)


class CreationMenu(QMenu):
    def __init__(self):
        super(CreationMenu, self).__init__()
        self.constraints = constraint_widgets()
        self.act = {}

        for k in sorted(self.constraints.keys()):
            self.act[k] = QAction(self)
            self.addAction( self.act[k] )
            self.act[k].setText( k )


class ObjWidget(QWidget):
    def __init__(self, name=None):
        super(ObjWidget, self).__init__()
        self.icon_layout = QHBoxLayout()
        self.icon_layout.setSpacing(2)
        self.title = QToolButton()

        self.title_font = QFont()
        self.title_font.setPointSize(14)
        self.title_font.setFamily("Courier")
        self.title.setAutoRaise(True)
        #self.title.setSizePolicy(QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed))
        self.title.setFont( self.title_font )
        self.title.setText( str(name) )
        self.title.setMinimumHeight(30)
        self.derp = QPushButton("well derpy derpy")
        self.tb = QToolButton()
        self.tb.setText("V")
        self.tb.setMinimumSize(46,46)
        
        self.id = str(uuid.uuid4())

        self.master_layout = QVBoxLayout()
        shrink_wrap(self.master_layout)
        self.icon_layout.addWidget(self.tb)
        self.icon_layout.setSpacing(5)
        self.icon_layout.addLayout(self.master_layout)
        self.master_layout.setSpacing(2)
        self.setLayout(self.icon_layout)

        self.master_layout.addWidget(self.title)
        self.master_layout.addWidget(self.derp)


class ItemList(QWidget):
    def __init__(self, parent=None):

        super(ItemList, self).__init__()

        self.master_layout = QVBoxLayout()

        shrink_wrap(self.master_layout)
        self.setLayout( self.master_layout )
        self.lw = QListWidget()
        self.parent = parent
        self.ls = {}
        self.setFixedWidth(500)


        self.title = QLineEdit('derp')
        self.master_layout.addWidget( self.title )
        self.master_layout.addWidget( self.lw)
        self.lw.setDragDropMode(QAbstractItemView.InternalMove)
        self.lw.setResizeMode(QListView.Adjust)

        self.cmd = {"object": ObjWidget}
        for c, w in constraint_widgets().iteritems():
            self.cmd[c] = w
            self.add_item( c, c)

        
    def add_item(self,  typ=None, name="Item"):
        if typ:
            if typ in self.cmd.keys():
                o = self.cmd[typ]()
                o.set_name(name)
        else:
            o = ObjWidget(name)
        
        self.ls[o.id] = {}
        self.ls[o.id]['widget'] = o
        self.ls[o.id]['item_widget'] = QListWidgetItem()
        #self.ls[o.id]['item_widget'].setSizeHint()

        self.ls[o.id]['item_widget'].setSizeHint(self.ls[o.id]["widget"].sizeHint())

        self.lw.addItem(self.ls[o.id]['item_widget'])
        self.lw.setItemWidget( self.ls[o.id]['item_widget'], self.ls[o.id]['widget'])

    def add_factory(self):
        self.add_item(typ="object")

    def add_number(self):
        self.add_item(typ="number")
        
class Creator(QListWidget):
    def __init__(self):
        pass

    def add_widget(self):
        pass

class Window(QMainWindow):
    def __init__(self):
        super(Window, self).__init__()
        self.main = QWidget()
        self.setCentralWidget(self.main)
        self.logo = QLabel("aleksandra")
        self.logo_font = QFont()
        self.logo_font.setPointSize(24) 
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


        self.add = QToolButton()
        self.add.setText("+")

        self.setMinimumWidth(700)
        self.setMinimumHeight(500)

        self.master_layout = QVBoxLayout()
        self.il = ItemList(self)

        self.add_menu = CreationMenu()
        for a in self.add_menu.act.keys():
            self.add_menu.act[a].triggered.connect(self.il.add_item)



        self.scroll = QScrollArea(alignment=Qt.Horizontal)
        self.mil_col_widget = QWidget()

        self.mil_col = QHBoxLayout(self.mil_col_widget)
        shrink_wrap(self.mil_col)
        
        self.scroll.setWidget(self.mil_col_widget)
        self.scroll.setWidgetResizable(True)
        self.mil_col.addWidget(self.il)
        self.mil_col.addStretch()

        self.add.setMenu( self.add_menu )
        self.add.setPopupMode(QToolButton.InstantPopup)

 
        self.master_layout.addWidget( self.logo )
        self.master_layout.addWidget( self.add )
        self.master_layout.addWidget( self.scroll)
        self.main.setLayout( self.master_layout )

    def add_list(self):

        ind = len(self.stack_level.keys())+1
        self.stack_level[ind] = ItemList(self)
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

