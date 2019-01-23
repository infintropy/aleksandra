import sys
from widgets import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import * 
import inspect
import aleksa




class List(Constraint):
    def __init__(self, **kwargs):
        super(List, self).__init__(**kwargs)
        self.set_color("green")
        self.ls = {}
        self.list_height = 0
        self.widget_1 = QListWidget()
        self.widget_1.setMaximumHeight(self.list_height)
        self.widget_1.setSizePolicy( QSizePolicy.Expanding, QSizePolicy.Minimum )


        self.master_layout.addWidget(self.widget_1)
        self.widget_1.setDragDropMode(QAbstractItemView.InternalMove)
        self.add_obj = QToolButton()
        self.add_obj.setText("+")
        self.title.label.master_layout.addWidget(self.add_obj)

        self.add_obj.clicked.connect( self.add_item )
        self.setSizePolicy( QSizePolicy.Expanding, QSizePolicy.Minimum )

    def add_item(self, name="Item"):

        o = self.root.add_object(constraint=self, name=name, index=1)
        
        self.ls[o.id] = {}
        self.ls[o.id]['widget'] = o
        self.ls[o.id]['item_widget'] = QListWidgetItem()
        self.ls[o.id]['item_widget'].setSizeHint(self.ls[o.id]["widget"].sizeHint())
        self.ls[o.id]['item_widget'].setSizeHint(QSize( 0, 35 ))
        self.widget_1.addItem(self.ls[o.id]['item_widget'])
        self.widget_1.setItemWidget( self.ls[o.id]['item_widget'], self.ls[o.id]['widget']) 

        oid = self.root.constraints[self.id]['parent']
        iliw = self.root.constraints[self.id]['item_widget']
        iliw.setSizeHint(QSize(0,self.height()+35))
        self.list_height+=35
        
        self.widget_1.setMaximumHeight(self.list_height+2)
        ilid = self.root.objects[oid]['item_list']
        self.root.item_lists[ilid]['widget'].update()



class Choice(Constraint):
    def __init__(self, items=None, **kwargs):
        super(Choice, self).__init__(**kwargs)
        self.widget_1 = QComboBox()
        self.set_color("blue")
        if items:
            self.widget_1.addItems(items)
        else:
            self.widget_1.addItems(["Choice%d" %d for d in range(5)])
        self.master_layout.addWidget(self.widget_1)


class ImageGrid(Constraint):
    def __init__(self, items=None, **kwargs):
        super(ImageGrid, self).__init__(**kwargs)
        self.set_color("red", "orange")
        self.add_img = QToolButton()
        self.add_img.setText("+")
        self.title.label.master_layout.addWidget(self.add_img)
        self.add_img.clicked.connect( self.add_image )
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

    def add_image(self):
        a = QPushButton('derp')
        a.setMinimumHeight(18)
        self.master_layout.addWidget(a)
        oid = self.root.constraints[self.id]['parent']
        iliw = self.root.constraints[self.id]['item_widget']
        iliw.setSizeHint(QSize(0,self.height()+30))
        ilid = self.root.objects[oid]['item_list']
        self.root.item_lists[ilid]['widget'].update()



class GIF(Constraint):
    def __init__(self, items=None, **kwargs):
        super(GIF, self).__init__(**kwargs)
        """
        self.movie_screen = QLabel()
        self.movie_screen.setMaximumWidth(300)
        self.movie = QMovie("/Users/donaldstrubler/Downloads/fieri.gif", QByteArray()) 
        self.movie.setCacheMode(QMovie.CacheAll) 
        self.movie.setSpeed(100) 
        self.movie_screen.setMovie(self.movie) 
        self.movie.start()
        self.master_layout.addWidget(self.movie_screen)
        """

class TextLine(Constraint):
    def __init__(self, **kwargs):
        super(TextLine, self).__init__(**kwargs)
        self.set_color("teal", "purple")
        self.widget_1 = QLineEdit()
        self.master_layout.addWidget(self.widget_1, stretch=0)
        self.master_layout.addStretch()


class TextBlock(Constraint):
    def __init__(self, **kwargs):
        super(TextBlock, self).__init__(**kwargs)
        
        self.widget_1 = QPlainTextEdit()
        self.set_color("teal")
        self.master_layout.addWidget(self.widget_1, stretch=0)
        self.master_layout.addStretch()
        self.widget_1.setMaximumHeight(100)

class Number(Constraint):
    def __init__(self, **kwargs):
        super(Number, self).__init__(**kwargs)
        self.set_color("yellow")
        self.id = str(uuid.uuid4())
        self.widget_1 = QSpinBox()
        self.master_layout.addWidget(self.widget_1)


class Price(Constraint):
    def __init__(self, **kwargs):
        super(Price, self).__init__(**kwargs)
        self.layout = QHBoxLayout()
        self.set_color("orange")
        shrink_wrap(self.layout, margin=0, spacing=0)
        self.id = str(uuid.uuid4())
        self.symbol = QToolButton()
        self.symbol.setText("$")
        self.symbol.setFont(BUTTON_FONT)
        self.widget_1 = QSpinBox()
        self.layout.addWidget(self.symbol)
        self.layout.addWidget(self.widget_1)
        self.master_layout.addLayout(self.layout)

class File(Constraint):
    def __init__(self, **kwargs):
        super(File, self).__init__(**kwargs)

        self.layout = QHBoxLayout()
        self.file_path = QLineEdit()
        self.file_path.setPlaceholderText("/path/to/file.txt")
        self.master_layout.addWidget(self.file_path)

class Object(Constraint):
    def __init__(self, name=None, **kwargs):
        super(Object, self).__init__(**kwargs)

        self.mousePressEvent = self._emit_id


        
        self.obj = self.root.add_object(constraint=self, name=name, index=1)

        self.master_layout.addWidget( self.obj )
        self.title.setVisible(False)

    def _emit_id(self, e):
        self.root.show_object_item_list(self.obj)
        #print("(%s) level: %s" %(self.level, self.id ))
        self.mouseReleaseEvent(e)
        


class ScreenLocation(Constraint):
    def __init__(self, **kwargs):
        super(ScreenLocation, self).__init__(**kwargs)
        """
        USL     UC      USR
        CSL     C       CSR
        LSL     LC      LCR
        """
        self.ak = aleksa.ScreenLocation()
        self.depth_options = self.ak._z_possibilities

        self.buttons = {"USL" : (1,1),
                        "UC"  : (1,2),
                        "USR" : (1,3),
                        "CSL" : (2,1),
                        "C"   : (2,2),
                        "CSR" : (2,3),
                        "LSL" : (3,1),
                        "LC"  : (3,2),
                        "LCR" : (3,3)
                        }
        self.layout = QHBoxLayout()
        shrink_wrap(self.layout)
        self.button_layout = QGridLayout()
        for k,v in self.buttons.items():
            but = QToolButton()
            but.setFixedWidth(30)
            but.setFixedHeight(30)
            but.setText(k)
            but.setCheckable(True)
            self.button_layout.addWidget( but, v[0], v[1] )

        self._z_combo = QComboBox()
        for c,d in enumerate(["BG", "MG", "FG"]):
            self._z_combo.addItems([i for i in self.depth_options if d in i])
        self._z_combo.insertSeparator(5)
        self._z_combo.insertSeparator(11)
        self.layout.addLayout( self.button_layout )
        self.layout.addWidget( self._z_combo)
        self.master_layout.addLayout(self.layout)

