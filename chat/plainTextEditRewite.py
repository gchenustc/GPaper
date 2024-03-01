from PySide6.QtWidgets import QPlainTextEdit
from PySide6.QtGui import QKeyEvent
from PySide6.QtCore import Qt

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
