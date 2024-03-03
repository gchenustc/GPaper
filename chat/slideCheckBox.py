from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QCheckBox
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


        # 设置初始为关闭状态的图标
        self.setIcon(QIcon("images/switch_off.png"))
        self.setIconSize(QSize(36, 36))  # 自定义图标大小

        # 关联切换信号与槽函数
        self.stateChanged.connect(self.on_state_changed)

    def on_state_changed(self, state):
        """
        当开关状态改变时触发的槽函数
        参数state是一个枚举值，0表示未选中（关闭），2表示选中（开启）
        """
        if state == 2:
            self.setIcon(QIcon("images/switch_on.png"))  # 设置为开启状态的图标
        else:
            self.setIcon(QIcon("images/switch_off.png"))  # 设置为关闭状态的图标