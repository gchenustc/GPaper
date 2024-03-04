from PySide6.QtWidgets import QCheckBox
from PySide6.QtGui import QIcon
from PySide6.QtCore import QSize

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