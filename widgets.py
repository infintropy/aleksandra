import uuid
from PyQt5.QtCore import *
from PyQt5.QtWidgets import * 
from PyQt5.QtGui import * 

from fields import *

import six
import inspect
import sys
import os
import random
from utils import COLORS, icon, shrink_wrap


ICON_BASE = "/Users/donaldstrubler/PycharmProjects/nukemoji/lib_128/"
#ICON_BASE = "C:/Users/dstrubler/Downloads/EmojiOne_4.0_128x128_png/EmojiOne_4.0_128x128_png"
ICONS = os.listdir( ICON_BASE )

#########
### FONTS
#########
BUTTON_FONT = QFont()
BUTTON_FONT.setFamily('Helvetica')
BUTTON_FONT.setPointSize(13)




def CreateMenu(QMenu):
    def __init__(self):
        super(CreateMenu, self).__init__()

        pass



class ColorMenu(QMenu):
    def __init__(self):
        super(ColorMenu, self).__init__()

        self.color_bar = QToolBar()

        for color, vals in COLORS.items():
            act = QToolButton()

            pix = QPixmap(9,9)
            pix.fill( QColor(vals[0], vals[1], vals[2]) )
            icon = QIcon(pix)
            act.setIcon( icon )


            self.color_bar.addWidget(act )
        
        self.color_bar.setIconSize(QSize(9,9))


        self.wAction = QWidgetAction(self)
        self.wAction.setDefaultWidget(self.color_bar)

        self.addAction( self.wAction )

class Evaluation():
    pass


class Icon(QToolButton):
    def __init__(self):
        super(Icon, self).__init__()
        self.setText("i")
        self.ic = QIcon("%s/%s" %(ICON_BASE, random.choice(ICONS)))
        #self.ic = QIcon()
        self.setIcon( self.ic )
        self.setIconSize(QSize(30,30))
        self.setAutoRaise(True)


class TagBar(QWidget):
    def __init__(self, *tags):
        super(TagBar, self).__init__()   
        self.master_layout = QHBoxLayout()
        shrink_wrap(self.master_layout, spacing=0, margin=0)
        self.setLayout(self.master_layout)
        self.add = QToolButton()
        self.add.setText("+")
        self.add.setStyleSheet("background-color:rgba(10, 30, 40, 10);")
        #self.master_layout.addWidget( self.add  )
        self.tags = []
        #self.add.clicked.connect( self.add_tag )

    def add_tag(self, tag='tag'):
        if not tag:
            tag = "dawg!"
        tag_button = QToolButton()
        tag_button.setAutoRaise(True)
        self.tags.append(tag_button)
        tag_button.setStyleSheet("background-color:rgba(40, 60, 20, 100);")
        tag_button.setText("#" +tag)
        tag_button.setMinimumHeight(20)
        self.master_layout.addWidget(tag_button)

class NameBadge(QWidget):
    def __init__(self, label=None):
        super(NameBadge, self).__init__()
        self.label = QToolButton()
        self.label.setStyleSheet("background-color:rgba(50,50,50,120);border-radius:4px;QToolButton::menu-indicator { image: none; }")
        self.label.setFont( BUTTON_FONT )
        self.label.setAutoRaise(True)
        #self.label.setPopupMode(QToolButton.InstantPopup)


        self.tag_bar = TagBar()
        self.tag_bar.add_tag("test!")


        self.fav = QToolButton(  )
        self.fav.setText( "<3" )
        self.fav.setCheckable(True)

        self.req = QToolButton()
        self.req.setText("+")
        
        self.req.setCheckable(True)




        self.cmenu = ColorMenu()
        self.label.setMenu( self.cmenu )
        self.act_fav = QAction(self.cmenu)
        self.act_fav.setText("make favorite")

        self.act_tag = QAction(self.cmenu)
        self.act_tag.setText("add tag")

        self.cmenu.addAction(self.act_fav)
        self.cmenu.addAction(self.act_tag)

        self.act_tag.triggered.connect(self.tag_bar.add_tag)



        self.label.setText("button")
        self.master_layout = QHBoxLayout()
        self.master_layout.addWidget(self.label)
        self.master_layout.addWidget(self.tag_bar)


        self.master_layout.addStretch()
        #self.master_layout.addWidget( self.req)
        #self.master_layout.addWidget( self.fav )

        self.setLayout(self.master_layout)
        self.label.setMinimumHeight(20)
        self.label.setMaximumHeight(20)

        shrink_wrap(self.master_layout)

        self.favorite = QToolButton()
        self.favorite.setText("*")

    def add_favorite(self):
        pass


class EditLabel(QStackedWidget):

    edited = pyqtSignal(str)

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

    def text(self):
        return self.label.label.text()

    def edit_text(self, event):
        self.setCurrentWidget( self.edit )

    def commit_text(self):
        self.setCurrentWidget( self.label )
        self.set_text( self.edit.text() )
        self.edited.emit("derp!")

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
        
        shrink_wrap(self.master_layout, margin=5, spacing=3)
        self.master_layout.setContentsMargins(10,1,5,1)
        self.setLayout( self.master_layout )

        self.check = QCheckBox()
        self.expand = QToolButton()
        self.expand.setIcon(QIcon(QPixmap( icon("next") )))
        self.expand.setAutoRaise(True)



        self.master_layout.addWidget( self.check )
        self.master_layout.addWidget( self.label )
        self.master_layout.addStretch()
        self.master_layout.addWidget(self.expand)

        self.mousePressEvent = self._emit_id

        self.expand.clicked.connect( self.make_list )
        self.label.edited.connect( self.label_edited )



    
    def label_edited(self, t):
        try:
            ilid = self.root.objects[self.id]["item_list"]
            il = self.root.item_lists[ilid]['widget']
            il.title.set_text( self.label.text() )
        except:
            pass

    def _emit_id(self, event):
        self.root.show_object_item_list(self)
        print("(%s) level: %s" %(self.level, self.id ))
        self.validate_children()
        self.mouseReleaseEvent(event)
        

    def make_list(self):
        self.root.show_object_item_list(self, make=True)

    def object_focus(self):
        self.root.object_focus(self.id)

    def add_constraint(self, typ="List"):
        cons = self.root.add_constraint(obj=self, typ=typ)

    def get_constraints(self):
        print('THESE ARE THE CONSTRAINTS')
        return [v['widget'] for i,v in self.root.constraints.items() if v['parent'] == self.id]

    def validate_children(self):
        for const in self.get_constraints():
            print(const.validate())

class Constraint(QWidget):
    def __init__(self, parent=None, level=9000, **kwargs):
        super(Constraint, self).__init__(**kwargs)
        self.color_bar = QWidget()
        self.level = level

        


        #print("Constraint being created, level %d" %self.level)
        self.color_bar.setFixedWidth(6)
        self.set_color("orange")
        self.parent = parent
        self.ctrl_dots = QLabel(" ::")
        self.root = self.parent
        self.id = str(uuid.uuid4())
        self.name = None
        self.meta_layout = QHBoxLayout()
        shrink_wrap(self.meta_layout, margin=2, spacing=5)
        #self.ctrl_dots = QLabel(" ::")
        self.grab_layout = QVBoxLayout()
        self.icon_layout = QVBoxLayout()
        self.grab_layout.setContentsMargins(0,15,0,0)
        self.icon_layout.setContentsMargins(0,5,0,0)
        self.icon = Icon()

        self.meta_layout.addWidget(self.color_bar)
        #self.meta_layout.addLayout(self.grab_layout)
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
        self.title.set_text(self.__class__.__name__)
        self._name = None                                   
        self.master_layout.addWidget(self.title, stretch=0)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        #self.mouseReleaseEvent = self._emit_id

    def set_color(self, *colors):
        r = sum([COLORS[c][0] for c in colors])/len(colors)
        g = sum([COLORS[c][1] for c in colors])/len(colors)
        b = sum([COLORS[c][2] for c in colors])/len(colors)
        self.color_bar.setStyleSheet("background-color:rgb(%d, %d, %d);border-radius:3px" %(r,g,b))

    def set_name(self, nm):
        self._name = nm
        self.title.set_text( self._name )

    def validate(self):
        #reimplement in subclass
        return True

    
    def _emit_id(self, event):
        print(self.root.objects)



