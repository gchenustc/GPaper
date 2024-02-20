from PySide6.QtWidgets import QApplication, QPushButton
from PySide6.QtCore import Qt
from PySide6 import QtGui

class CustomPushButton(QPushButton):
    def focusInEvent(self, event: QtGui.QFocusEvent):
        print(f"{self.text()} gained focus.")
        super().focusInEvent(event)  # 调用父类的实现以保持默认行为

app = QApplication([])

button = CustomPushButton("Hello, Button!")
button.setFocusPolicy(Qt.StrongFocus)  # 或者Qt.TabFocus，根据你的需求

button.show()

app.exec_()