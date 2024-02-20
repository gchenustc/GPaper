from PySide6.QtCore import (Signal, QCoreApplication, QMetaObject,  QRect, QSize)
from PySide6.QtGui import (QIcon)
from PySide6.QtWidgets import (QApplication, QPushButton, QMessageBox,
                              QTextEdit, QWidget)
from dao import paperDao


class PaperTextManageWidget(QWidget):
    editChangedSignal = Signal()

    def __init__(self, paperTable=None, paperId=-1):
        super().__init__()
        self.paperTable = paperTable

        self.paperId = paperId

        self.setupUi()

        self.clearBtn.clicked.connect(self.clearBtnClicked)
        self.confirmBtn.clicked.connect(self.confrimBtnClicked)

        self.initPaperText()

    def setupUi(self):

        self.setObjectName(u"Form")
        self.resize(1000, 760)
        self.textEdit = QTextEdit(self)
        self.textEdit.setObjectName(u"textEdit")
        self.textEdit.setGeometry(QRect(30, 30, 940, 660))

        self.clearBtn = QPushButton(self)
        self.clearBtn.setObjectName(u"pushButton")
        self.clearBtn.setGeometry(QRect(350, 710, 75, 31))
        icon = QIcon()
        icon.addFile(u"./images/clear.png", QSize(), QIcon.Normal, QIcon.Off)
        self.clearBtn.setIcon(icon)

        self.confirmBtn = QPushButton(self)
        self.confirmBtn.setObjectName(u"pushButton_2")
        self.confirmBtn.setGeometry(QRect(610, 710, 75, 31))
        icon1 = QIcon()
        icon1.addFile(u"./images/confirm.png",
                      QSize(), QIcon.Normal, QIcon.Off)
        self.confirmBtn.setIcon(icon1)

        self.retranslateUi(self)

        QMetaObject.connectSlotsByName(self)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate(
            "Form", u"Paper Detail", None))
        self.clearBtn.setText(
            QCoreApplication.translate("Form", u"clear", None))
        self.confirmBtn.setText(
            QCoreApplication.translate("Form", u"confirm", None))

    def clearBtnClicked(self):
        self.textEdit.clear()

    def confrimBtnClicked(self):
        paper = paperDao.getPaperFromId(self.paperId)[0]

        paper.text = self.textEdit.toPlainText().strip()

        if not paperDao.modifyPaper(paper):
            QMessageBox.critical(
                None, "Error", "Failed to modify paper into database")
            return
        QMessageBox.information(None, "Success", "Modify paper successfully")

        self.editChangedSignal.emit()

    def initPaperText(self):
        paper = paperDao.getPaperFromId(self.paperId)[0]
        self.textEdit.setPlainText(paper.text)


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    ui = PaperTextManageWidget()
    ui.show()
    sys.exit(app.exec())
