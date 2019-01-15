import uuid
from PyQt5.QtCore import *
from PyQt5.QtWidgets import * 
from PyQt5.QtGui import * 
import six
import inspect
import sys
import os
import random


#ICON_BASE = "/Users/donaldstrubler/PycharmProjects/nukemoji/lib_128/"
ICON_BASE = "C:/Users/dstrubler/Downloads/EmojiOne_4.0_128x128_png/EmojiOne_4.0_128x128_png"
ICONS = os.listdir( ICON_BASE )

#########
### FONTS
#########
BUTTON_FONT = QFont()
BUTTON_FONT.setFamily('Helvetica')
BUTTON_FONT.setPointSize(13)


COLORS = {  "red"       : (165, 66, 61),
            "orange"    : (194, 115, 59),
            "yellow"    : (226, 184, 67),
            "olive"     : (192, 201, 81),
            "green"     : (87, 178, 98),
            "teal"      : (75, 206, 192),
            "blue"      : (78, 131, 168),
            "violet"    : (99, 72, 143),
            "purple"    : (136, 75, 147),
            "pink"      : (161, 65, 112),
            "brown"     : (145, 108, 81)
}


def shrink_wrap(layout, margin=2, spacing=2):
    """

    """
    layout.setContentsMargins(margin,margin,margin,margin)
    layout.setSpacing(spacing)





class Icon(QToolButton):
    def __init__(self):
        super(Icon, self).__init__()
        self.setText("i")
        self.ic = QIcon("%s/%s" %(ICON_BASE, random.choice(ICONS)))
        #self.ic = QIcon()
        self.setIcon( self.ic )
        self.setIconSize(QSize(30,30))
        self.setAutoRaise(True)






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

        self.setMaximumHeight(25)

        self.label.label.setFont(BUTTON_FONT)

        self.addWidget( self.label)
        self.addWidget( self.edit )

        self.label.label.setText("button")

        self.label.label.mouseDoubleClickEvent = self.edit_text

        #self.label.label.clicked.connect(self.edit_text)
        self.edit.editingFinished.connect( self.commit_text )

    def edit_text(self, event):
        self.setCurrentWidget( self.edit )

    def commit_text(self):
        self.setCurrentWidget( self.label )
        self.set_text( self.edit.text() )

    def set_text(self, txt):
        self.label.label.setText(txt)
        self.edit.setText(txt)

class ObjWidget(QWidget):

    def __init__(self, parent=None, name=None, level=9000):
        super(ObjWidget, self).__init__()
        self.parent = parent
        self.root = self.parent
        self.level = level
        print("Object being created. Level %d" %self.level)
        self.id = str(uuid.uuid4())
        self.master_layout = QHBoxLayout()
        self.label = EditLabel()
        self.label.set_text("Item")
        self.master_layout.addWidget( self.label )
        shrink_wrap(self.master_layout, margin=5, spacing=3)
        self.setLayout( self.master_layout )

        self.mousePressEvent = self._emit_id
    


    def _emit_id(self, event):
        self.root.show_object_item_list(self)
        print("(%s) level: %s" %(self.level, self.id ))
        self.mouseReleaseEvent(event)

    def object_focus(self):
        self.root.object_focus(self.id)

    def add_constraint(self, typ="List"):
        cons = self.root.add_constraint(obj=self, typ=typ)

class Constraint(QWidget):
    def __init__(self, parent=None, level=9000, **kwargs):
        super(Constraint, self).__init__(**kwargs)
        self.color_bar = QWidget()
        self.level = level
        print("Constraint being created, level %d" %self.level)
        self.color_bar.setFixedWidth(6)
        self.set_color("orange")
        self.parent = parent
        
        self.root = self.parent
        self.id = str(uuid.uuid4())
        self.name = None
        self.meta_layout = QHBoxLayout()
        shrink_wrap(self.meta_layout, margin=2, spacing=5)
        self.ctrl_dots = QLabel(" ::")
        self.grab_layout = QVBoxLayout()
        self.icon_layout = QVBoxLayout()
        self.grab_layout.setContentsMargins(0,15,0,0)
        self.icon_layout.setContentsMargins(0,5,0,0)
        self.icon = Icon()

        self.meta_layout.addWidget(self.color_bar)
        self.meta_layout.addLayout(self.grab_layout)
        self.meta_layout.addLayout(self.icon_layout)

        self.grab_layout.addWidget( self.ctrl_dots )
        self.grab_layout.addStretch(1)
        self.icon_layout.addWidget( self.icon )
        self.icon_layout.addStretch(1)

        self.master_layout = QVBoxLayout()
        self.meta_layout.addLayout(self.master_layout)
        self.setLayout(self.meta_layout)
        shrink_wrap(self.master_layout, margin=2, spacing=2)
        self.title = EditLabel()
        self._name = None                                   
        self.master_layout.addWidget(self.title, stretch=0)
        
        #self.mouseReleaseEvent = self._emit_id

    def set_color(self, color):
        if color in list(COLORS.keys()):
            c = COLORS[color]
            self.color_bar.setStyleSheet("background-color:rgb(%d, %d, %d);border-radius:3px" %(c[0], c[1], c[2]))

    def set_name(self, nm):
        self._name = nm
        self.title.set_text( self._name )

    


    
    def _emit_id(self, event):
        print(self.root.objects)



