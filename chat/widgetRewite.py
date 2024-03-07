from PySide6.QtWidgets import QPlainTextEdit, QLabel, QMenu, QVBoxLayout, QWidget, QCheckBox
from PySide6.QtGui import QKeyEvent, QColor, QCursor, QPalette, QIcon
from PySide6.QtCore import Qt, QSize

class MyPlainTextEdit(QPlainTextEdit):

    def __init__(self,parent=None):
        super(MyPlainTextEdit, self).__init__(parent)

    # rewrite keyPressEvent function
    def keyPressEvent(self, event: QKeyEvent):
        if self.toPlainText() and event.key() == Qt.Key_Return and event.modifiers() == Qt.ControlModifier:
            self.sendMessages()                                         
        elif event.key() == Qt.Key_Return:
            self.insertPlainText('\n')
        else:
            super().keyPressEvent(event)

    def sendMessages(self):
        self.setEnabled(False) # disable the input
        self.setUndoRedoEnabled(False)
        self.setUndoRedoEnabled(True) # set focus

class MyLabel(QLabel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setContextMenuPolicy(Qt.CustomContextMenu)  # 设置右键菜单策略
        self.customContextMenuRequested.connect(self.showContextMenu)
        
        self.setStyleSheet("QLabel { background-color : #FFFFFF;}")  # 设置初始样式
        self.normal_color = QColor("#FFFFFF")  # 记录正常状态下的背景颜色
        self.hover_color = QColor("#DDEEFF")  # 设置鼠标悬停时的背景颜色

    def enterEvent(self, event):
        self.setStyleSheet(f"QLabel {{ background-color : {self.hover_color.name()}; }}")  # 鼠标进入时改变背景色

    def leaveEvent(self, event):
        self.setStyleSheet(f"QLabel {{ background-color : {self.normal_color.name()}; }}")  # 鼠标离开时恢复背景颜色

    def showContextMenu(self, pos):
        menu = QMenu(self)

        action1 = menu.addAction("select")
        action2 = menu.addAction("delete")

        # 添加动作的槽函数（这里仅作演示，未添加实际槽函数）
        # action1.triggered.connect(some_function)
        # action2.triggered.connect(another_function)

        menu.exec_(self.mapToGlobal(pos))  # 在鼠标点击的位置显示菜单


class SlideCheckBox(QCheckBox):
    def __init__(self, parent=None):
        super(SlideCheckBox, self).__init__(parent)
        
        # raise caution: QPainter::begin: Paint device returned engine == 0, type: 3
        self.setStyleSheet("""
            QCheckBox::indicator {
                width: 0;
                height: 0;
                margin: 0;
            }
        """)


        # set the init icon
        self.setIcon(QIcon("images/switch_off.png"))
        self.setIconSize(QSize(36, 36)) 

        # ! connect the the state change function
        self.stateChanged.connect(self.on_stateChanged)

    def on_stateChanged(self, state):
        if state == 2:
            self.setIcon(QIcon("images/switch_on.png"))
        else:
            self.setIcon(QIcon("images/switch_off.png"))
