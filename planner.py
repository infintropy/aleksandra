from PyQt5.QtCore import *
from PyQt5.QtWidgets import * 
from PyQt5.QtGui import *
import datetime
import os
import sys
import uuid
import random

class DayItem(QTableWidget):
    write_log = pyqtSignal(int)
    scroll_to_hour = pyqtSignal(str)
    def __init__(self, parent, date=None):
        super(DayItem, self).__init__()
        self.parent = parent
        self.events = {}


        self.agenda = {}
        hours = list(range(1, 25))
        # self.schedule.setRowCount( len( days ) )
        c = 0
        hrz = [12] + (list(range(1, 13)) * 2)[:-1]
        self.hour_readable = ["%s AM" % str(q) if i < 12 else "%s PM" % str(q) for i, q in enumerate(hrz)]
        self.setColumnCount(3)
        self.verticalHeader().hide()

        self.setHorizontalHeaderLabels(['Time', 'tbd', 'Agenda'])
        self.horizontalHeaderItem(0).setTextAlignment(Qt.AlignHCenter)

        night = QColor(205, 220, 255, 170)
        morning = QColor(255, 245, 130, 180)
        afternoon = QColor(255, 165, 90, 160)
        evening = QColor(210, 150, 180, 190)

        for hour in hours:

            self.insertRow(c)

            t = QTableWidgetItem(self.hour_readable[c])

            t.setTextAlignment(Qt.AlignVCenter | Qt.AlignRight)
            t.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            font = QFont()
            font.setPointSize(10)
            font.setBold(False)

            self.agenda[c] = AgendaItem(self.parent, c)
            self.agenda[c].hourDoubleClicked.connect(self.add_event)
            self.agenda[c].cellSelected.connect(self.select_row)
            self.setCellWidget(c, 2, self.agenda[c])

            # s.setMinimumHeight(30)
            if c < 6:
                t.setForeground(QBrush(night))
            if c == 6:
                t.setForeground(QBrush(self.mix_colors(night, morning, (0.7, 0.3))))
            if c > 6 and c < 15:
                t.setForeground(QBrush(morning))
            if c == 15:
                t.setForeground(QBrush(self.mix_colors(morning, afternoon, (0.5, 0.5))))
            if c > 15 and c < 19:
                t.setForeground(QBrush(afternoon))
            if c == 19:
                t.setForeground(QBrush(self.mix_colors(afternoon, evening, (0.5, 0.5))))
            if c > 19:
                t.setForeground(QBrush(evening))
            if c == 23:
                t.setForeground(QBrush(self.mix_colors(night, evening, (0.5, 0.5))))
            t.setBackground(QBrush(QColor(60, 60, 60, 80)))
            t.setFont(font)

            # if weekend day:
            if datetime.datetime.now().strftime("%w") in [0, 6]:
                if (c > 8 and c < 19):
                    t.setBackground(QBrush(QColor(100, 100, 100, 55)))
            # set the item.

            self.setItem(c, 0, t)
            c += 1
        self.setColumnWidth(0, 45)
        self.setColumnWidth(1, 35)
        self.resizeRowsToContents()
        self.resizeColumnToContents(2)
        # self.scroll_to_now()

        self.horizontalHeader().setStretchLastSection(True)

        self.sched_pal = self.palette()
        self.sched_pal.setColor(QPalette.Highlight, QColor(120, 120, 120, 15))
        self.setPalette( self.sched_pal )
        self.setSelectionBehavior(QAbstractItemView.SelectRows)

    def keyPressEvent(self, eventQKeyEvent):
        key = eventQKeyEvent.key()

        if key == Qt.Key_Left:
            self.move_horizontal(-1)
        if key == Qt.Key_Right:
                self.move_horizontal(1)
        if key == Qt.Key_Up:
            if eventQKeyEvent.modifiers() & Qt.ShiftModifier:
                self.move_event(-3)
            else:
                self.move_event(-1)
        if key == Qt.Key_Down:
            if eventQKeyEvent.modifiers() & Qt.ShiftModifier:
                self.move_event(3)
            else:
                self.move_event(1)

    def move_event(self, offset):
        for i,e in self.events.items():
            if e.isChecked():
                ind = e.hour
                if -1<(ind+offset)<24:
                    self.agenda[ind].master_layout.removeWidget(e)
                    e.set_hour( ind+offset )

                    self.scroll_to_hour.emit( self.hour_readable[ind+offset] )

                    self.agenda[ind+offset].master_layout.insertWidget(0, e)
        self.write_day_log()

    def move_horizontal(self, offset):
        for i, e in self.events.items():
            if e.isChecked():
                self.agenda[e.hour].move( e, offset )

        self.write_day_log()



    def mix_colors(self, color1, color2, mix):
        return QColor(mix[0] * color1.red() + mix[1]* color2.red(),
                      mix[0] * color1.green() + mix[1] * color2.green(),
                      mix[0] * color1.blue() + mix[1] * color2.blue(),
                      mix[0] * color1.alpha() + mix[1] * color2.alpha())

    def add_event(self, hour, string=None):
        if string:
            task_name = string
            ok = True
        else:
            task_name, ok = QInputDialog.getText(self, 'Task', 'name:')
            hour = hour.hour
        if ok:

            name = task_name
            event =  EventButton(self, name)
            name = event.id
            self.events[name] = event
            self.events[name].set_hour( hour )
            self.events[name].event_checked.connect( self.register_selection_choice )

            self.agenda[hour].master_layout.insertWidget( 0 , self.events[name])
            self.write_log.emit(1)

    def select_row(self, row):
        self.register_selection_choice(None, clear=True)
        self.selectRow(row)

    def register_selection_choice(self, button, clear=None):
        shift = None
        modifiers = QApplication.keyboardModifiers()
        if modifiers == Qt.ShiftModifier:
            shift=True
        if not shift:
            for i,e in self.events.items():

                if e.isChecked():


                    e.setChecked(False)
            if clear==None:

                if button.isChecked():

                    button.setChecked(False)
                else:
                    button.setChecked(True)

    def write_day_log(self):
        self.write_log.emit(1)





class AgendaItem(QWidget):

    hourDoubleClicked = pyqtSignal( object )
    cellSelected = pyqtSignal(int)

    def __init__(self, parent, hour):
        super(AgendaItem, self).__init__()

        self.master_layout = QHBoxLayout()
        self.items = {}
        self.hour = hour
        self.parent = parent

        self.loaded_hour = False


        self.master_layout.setContentsMargins( 10,0,3,0 )
        self.master_layout.setSpacing(6)


        self.setMinimumHeight( 40 )
        self.setMinimumWidth( 200 )

        self.setLayout( self.master_layout )

    def mousePressEvent(self, event):

        self.last = "Click"

    def mouseReleaseEvent(self, event):

        if self.last == "Click":
            self.cellSelected.emit(self.hour)
            QTimer.singleShot(QApplication.instance().doubleClickInterval(),
                              self.performSingleClickAction)
        else:
            self.hourDoubleClicked.emit( self )
            self.message = "Double Click"
            self.update()

    def mouseDoubleClickEvent(self, event):

        self.last = "Double Click"

    def performSingleClickAction(self):

        if self.last == "Click":

            self.update()

    def add_item_input(self):
        task_name, ok = QInputDialog.getText(self, 'Name Your Shirt', 'name:')
        if ok:
            self.add_item( task_name )

    def move(self, widget, direction=None):
        wdgs = self.master_layout.count()
        ind = 0
        for i in range(wdgs):

            if self.master_layout.itemAt(i).widget() is widget:

                ind = i

        #self.master_layout.removeWidget(widget)
        self.master_layout.insertWidget( ind+direction, widget)



    def add_item(self, name, event=None):
        #TODO:: make own class. Really needs to be a base level Event class, and then special "Apps" can make their own event interface, to preview the workflow.
        index = len(self.items.keys())
        if event:
            self.items[event.text()] = event
            self.items[event.text()].set_hour( self.hour )
            print("%s = %s" %(self.items[event.text()].text(),self.items[event.text()].hour ))
            self.master_layout.insertWidget(0, self.items[event.text()])
        else:
            font = QFont()
            font.setCapitalization( QFont.AllUppercase )

            font.setPixelSize( 11 )
            font.setLetterSpacing( QFont.AbsoluteSpacing, 1.1 )


            self.items[name] = EventButton(self, name)
            self.items[name].set_hour( self.hour )

            self.master_layout.insertWidget( 0  , self.items[name])



    def pop_item(self, event):
        #self.master_layout.removeWidget(event)
        del self.items[event.text()]


class EventButton(QToolButton):

    event_checked = pyqtSignal(object)

    def __init__(self, parent, name):
        super(EventButton, self).__init__()
        self.parent = parent
        self.hour = 0
        self.font = QFont()
        self.font.setCapitalization( QFont.AllUppercase )
        self.id = "%s.%s" %( str(uuid.uuid4()), name)

        self.font.setPixelSize( 11 )
        self.font.setLetterSpacing( QFont.AbsoluteSpacing, 1.1 )




        self.menu = QMenu()
        self.emoji_act = QAction( self.menu )
        self.emoji_act.setText('change emoji')

        self.setMenu( self.menu )

        self.bottom_menu = QToolBar()
        self.t1 = QAction(self.bottom_menu)
        self.t1.setText( "DONE" )
        self.t2 = QAction(self.bottom_menu)
        self.t2.setText( "START" )
        for t in [self.t1, self.t2]:
            self.bottom_menu.addAction(t)

        self.wAction = QWidgetAction(self)
        self.wAction.setDefaultWidget(self.bottom_menu)
        self.menu.addAction(self.wAction)
        self.menu.addAction( self.emoji_act )

        self.setPopupMode( QToolButton.MenuButtonPopup )

        toolbuttonSizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.setSizePolicy(toolbuttonSizePolicy)
        #meta # self.items[name] = QToolButton()
        self.setMinimumHeight(30)
        self.setFont( self.font )
        self.setAutoRaise(True)

        self.setCheckable(True)
        self.setAutoFillBackground(True)
        self.setStyleSheet( "background-color:rgba(85,90,100,100);" )
        if 'tgm' in name.lower():
            self.setStyleSheet("background-color:rgba(140,85,30,180);")
        if name.lower()=="sleep":
            self.setStyleSheet("background-color:rgba(50,60,80,90);")
        self.setText(name)
        self.set_emoji("kissing_cat")

        self.clicked.connect( self.send_self )

    def set_hour(self, hour):
        self.hour = hour

    def set_position(self, direction):
        pass


    def send_self(self):
        self.event_checked.emit(self)

    def make_small(self):
        toolbuttonSizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.setSizePolicy(toolbuttonSizePolicy)

    def set_emoji(self, emoji=None):

        path = self.parent.parent.emoji_util.get_path_from_keyword(random.choice( list(self.parent.parent.emoji_util.map.keys()) ).replace(":", ""))
        pxm = QPixmap(path)
        pxm.scaledToHeight(24, Qt.SmoothTransformation)
        icon = QIcon(pxm)
        self.setIcon( icon )
        self.setIconSize(QSize(24, 24))
        self.setToolButtonStyle( Qt.ToolButtonTextBesideIcon )

        palette = self.palette()


        palette.setBrush(self.backgroundRole(), QBrush(pxm));

        self.setPalette(palette)




        #set icon to emoji. This will be a standard used setting in subclasses
