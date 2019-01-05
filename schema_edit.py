import sys
from PySide.QtCore import *
from PySide.QtGui import *


class ObjWidget(QWidget):
    def __init__(self, name=None):
        super(ObjWidget, self).__init__()
        self.icon_layout = QHBoxLayout()
        self.icon_layout.setSpacing(2)
        self.title = QToolButton()
        self.title.setText( name )
        self.derp = QPushButton("well derpy derpy")
        self.tb = QToolButton()
        self.tb.setText("V")
        self.tb.setMinimumSize(45,45)
        self.setContentsMargins(1,1,1,1)


        self.master_layout = QVBoxLayout()
        self.icon_layout.addWidget(self.tb)
        self.icon_layout.addLayout(self.master_layout)
        self.master_layout.setSpacing(2)
        self.setLayout(self.icon_layout)

        self.master_layout.addWidget(self.title)
        self.master_layout.addWidget(self.derp)



class ItemList(QListWidget):
    def __init__(self):
        super(ItemList, self).__init__()
        self.itm = QListWidgetItem()
        self.itm.setSizeHint(QSize(50,70))
        self.addItem(self.itm)
        self.w = ObjWidget("RotoPaint")
        self.setItemWidget( self.itm, self.w)
        
class Creator(QListWidget):
    def __init__(self):
        pass

    def add_widget(self):
        pass

class Window(QWidget):
    def __init__(self):
        super(Window, self).__init__()

        self.stacker1 = QStackedWidget()
        self.stack_level = {1: self.stacker1}

        self.master_layout = QHBoxLayout()
        self.il = ItemList()

        self.master_layout.addWidget( self.il )
        self.setLayout( self.master_layout )




if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = Window()
    main.show()
    sys.exit(app.exec_())