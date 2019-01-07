import sys
from PySide2.QtCore import *
from PySide2.QtWidgets import *
from PySide2.QtGui import *
import qtmodern
import uuid
import theme

'''
Can be viewed as objects with attributes. 
Can be viewed as a dependency tree
'''


class Constraint(QWidget):
    def __init__(self, **kwargs):
        super(Constraint, self).__init__(**kwargs)

        self.master_layout = QHBoxLayout()

class cLineEntry(Constraint):
    def __init__(self, **kwargs):
        super(cLineEntry, self).__init__(**kwargs)
        self.id = str(uuid.uuid4())
        self.widget_1 = QLineEdit()
        self.master_layout.addWidget(self.widget_1)

class WidgetFactory(QWidget):
    def __init__(self):

        super(WidgetFactory, self).__init__()
        self.id = str(uuid.uuid4())
        self.master_layout = QFormLayout()
        self.widgets = {'cLineEntry': cLineEntry}
        self.canvas = {}
        
        self.setLayout = self.master_layout

        self.add('cLineEntry')

    def add(self, name):
        if self.widgets.get(name):
            print "adding!"
            item = self.widgets[name]()
            self.canvas[item.id] = item
            self.master_layout.addRow(name, item)




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
        self.setContentsMargins(1,1,1,1)
        self.id = str(uuid.uuid4())

        self.master_layout = QVBoxLayout()
        self.icon_layout.addWidget(self.tb)
        self.icon_layout.setSpacing(5)
        self.icon_layout.addLayout(self.master_layout)
        self.master_layout.setSpacing(2)
        self.setLayout(self.icon_layout)

        self.master_layout.addWidget(self.title)
        self.master_layout.addWidget(self.derp)




class ItemList(QListWidget):
    def __init__(self, parent=None):

        super(ItemList, self).__init__()
        self.parent = parent
        self.ls = {}
        self.setFixedWidth(250)
        self.add_item()

        self.setDragDropMode(QAbstractItemView.InternalMove)

        self.cmd = {"factory": WidgetFactory}

    def add_item(self, name="Item", typ=None):
        if typ:
            if typ in self.cmd.keys():
                o = WidgetFactory(  )
                #o = ObjWidget(name)
        else:
            o = ObjWidget(name)
        self.ls[o.id] = {}
        self.ls[o.id]['widget'] = o
        self.ls[o.id]['item_widget'] = QListWidgetItem()
        self.ls[o.id]['item_widget'].setSizeHint(QSize(50,70))

        self.addItem(self.ls[o.id]['item_widget'])
        self.setItemWidget( self.ls[o.id]['item_widget'], self.ls[o.id]['widget'])

    def add_factory(self):
        print "yay!!!"
        self.add_item(typ="factory")

        
class Creator(QListWidget):
    def __init__(self):
        pass

    def add_widget(self):
        pass

class Window(QWidget):
    def __init__(self):
        super(Window, self).__init__()
        self.logo = QLabel("aleksandra")
        self.logo_font = QFont()
        self.logo_font.setPointSize(24) 
        self.logo_font.setFamily("Courier")
        self.logo.setFont(self.logo_font)

        self.initial_object = QLineEdit()

        self.stacker1 = QStackedWidget()
        self.stack_level = {1: self.stacker1}

        self.add = QToolButton()
        self.add.setText("+")

        self.setMinimumWidth(700)
        self.setMinimumHeight(500)

        self.add_menu = QMenu()
        self.make_range = QAction(parent=self.add_menu)
        self.make_object = QAction(parent=self.add_menu)
        self.make_range.setText("add list >>")
        self.make_object.setText("make object")
        self.make_factory = QAction(parent=self.add_menu)
        self.make_var = QAction(parent=self.add_menu)
        self.make_factory.setText("make Factory")
        self.make_var.setText("make variable")

        self.add_menu.addAction(self.make_range)
        self.add_menu.addAction(self.make_object)
        self.add_menu.addAction(self.make_factory)
        self.add_menu.addAction(self.make_var)

        self.master_layout = QVBoxLayout()
        self.il = ItemList(self)
        self.scroll = QScrollArea(alignment=Qt.Horizontal)
        self.mil_col_widget = QWidget()
        self.mil_col = QHBoxLayout(self.mil_col_widget)
        
        self.scroll.setWidget(self.mil_col_widget)
        self.scroll.setWidgetResizable(True)
        self.mil_col.addWidget(self.il)
        self.mil_col.addStretch()

        self.make_object.triggered.connect(self.il.add_item)
        self.make_range.triggered.connect( self.add_list )
        self.make_factory.triggered.connect(self.il.add_factory)

        self.add.setMenu( self.add_menu )
        self.add.setPopupMode(QToolButton.InstantPopup)

 
        self.master_layout.addWidget( self.logo )
        self.master_layout.addWidget( self.add)
        self.master_layout.addWidget( self.scroll)
        self.setLayout( self.master_layout )

    def add_list(self):

        ind = len(self.stack_level.keys())+1
        self.stack_level[ind] = ItemList(self)
        self.mil_col.insertWidget( len(self.stack_level.keys())-1, self.stack_level[ind] )
   





if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = Window()

    app.setStyle("Fusion")
    theme.dark(app)




    window.show()
    app.exec_()