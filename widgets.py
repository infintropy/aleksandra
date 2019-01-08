from PySide.QtCore import *
from PySide.QtGui import * 

ICON_EX = "C:/Users/dstrubler/material-design-icons/device/drawable-hdpi/ic_battery_charging_60_white_48dp.png"

BUTTON_FONT = QFont()

BUTTON_FONT.setFamily('Helvetica')
BUTTON_FONT.setPointSize(13)

class Icon(QToolButton):
    def __init__(self):
        super(Icon, self).__init__()
        self.setText("i")
        self.ic = QIcon(ICON_EX)
        
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
