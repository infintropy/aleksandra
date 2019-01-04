import sys
from PySide.QtCore import *
from PySide.QtGui import *

class Window(QWidget):
    def __init__(self):
        super(Window, self).__init__()

        self.master_layout = QHBoxLayout()
        self.button = QPushButton("view")

        self.master_layout.addWidget( self.button )
        self.setLayout( self.master_layout )


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = Window()
    main.show()
    sys.exit(app.exec_())