from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
                            QMetaObject, QObject, QPoint, QRect,
                            QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
                           QFont, QFontDatabase, QGradient, QIcon,
                           QImage, QKeySequence, QLinearGradient, QPainter,
                           QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QMainWindow, QHBoxLayout, QLabel, QLineEdit,
                               QPushButton, QSizePolicy, QTextEdit, QVBoxLayout,
                               QWidget, QMessageBox)

from dao import paperTypeDao
from entity.paperTypeModel import PaperType


class Ui_MainWindow(QMainWindow):
    def __init__(self):
        super(Ui_MainWindow, self).__init__()
        self.setupUi()

    def setupUi(self):
        self.resize(1000, 760)

        font = QFont()
        font.setPointSize(12)

        self.centralwidget = QWidget(self)
        self.centralwidget.setObjectName(u"centralwidget")
        self.centralwidget.setStyleSheet(
            "border-image: url(./images/green_background.png)")
        self.setCentralWidget(self.centralwidget)

        # paper type name label
        self.paperTypeNameLabel = QLabel(self)
        self.paperTypeNameLabel.setObjectName(u"paperTypeNameLabel")
        self.paperTypeNameLabel.setGeometry(QRect(120, 140, 81, 21))
        self.paperTypeNameLabel.setFont(font)

        # description label
        self.paperTypeDescLabel = QLabel(self)
        self.paperTypeDescLabel.setObjectName(u"descriptionLabel")
        self.paperTypeDescLabel.setGeometry(QRect(120, 310, 91, 51))
        self.paperTypeDescLabel.setFont(font)
        self.paperTypeDescLabel.setWordWrap(True)

        # horizontal layout
        self.horizontalLayoutWidget = QWidget(self)
        self.horizontalLayoutWidget.setObjectName(u"horizontalLayoutWidget")
        self.horizontalLayoutWidget.setGeometry(QRect(350, 500, 311, 81))
        self.horizontalLayout = QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setSpacing(120)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(20, 20, 20, 20)

        # add button
        self.addBtn = QPushButton(self.horizontalLayoutWidget)
        self.addBtn.setObjectName(u"addBtn")
        self.addBtn.setFont(font)
        icon = QIcon()
        icon.addFile(u"./images/add.png", QSize(), QIcon.Normal, QIcon.Off)
        self.addBtn.setIcon(icon)

        # add button signal
        self.addBtn.clicked.connect(self.add)

        self.horizontalLayout.addWidget(self.addBtn)

        # reset button
        self.resetBtn = QPushButton(self.horizontalLayoutWidget)
        self.resetBtn.setObjectName(u"resetBtn")
        self.resetBtn.setFont(font)
        icon1 = QIcon()
        icon1.addFile(u"./images/reset.png", QSize(), QIcon.Normal, QIcon.Off)
        self.resetBtn.setIcon(icon1)

        # ! reset button signal
        self.resetBtn.clicked.connect(self.reset)

        self.horizontalLayout.addWidget(self.resetBtn)

        # vertical layout
        self.verticalLayoutWidget = QWidget(self)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.verticalLayoutWidget.setGeometry(QRect(230, 130, 551, 361))
        self.verticalLayout = QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setSpacing(30)
        self.verticalLayout.setObjectName(u"verticalLayout_3")
        self.verticalLayout.setContentsMargins(15, 15, 15, 15)

        # paperTypeNameInput line edit
        self.paperTypeNameInput = QLineEdit(self.verticalLayoutWidget)
        self.paperTypeNameInput.setObjectName(u"lineEdit")

        self.verticalLayout.addWidget(self.paperTypeNameInput)

        # paperTypeDescInput text edit
        self.paperTypeDescInput = QTextEdit(self.verticalLayoutWidget)
        self.paperTypeDescInput.setObjectName(u"textEdit")

        self.verticalLayout.addWidget(self.paperTypeDescInput)

        self.verticalLayout.setStretch(0, 1)

        self.retranslateUi()

        # QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self):
        self.setWindowTitle(QCoreApplication.translate(
            "Form", u"Add paper type", None))
        self.paperTypeNameLabel.setText(
            QCoreApplication.translate("Form", u"type name", None))
        self.paperTypeDescLabel.setText(
            QCoreApplication.translate("Form", u"description", None))
        self.addBtn.setText(QCoreApplication.translate("Form", u"add", None))
        self.resetBtn.setText(
            QCoreApplication.translate("Form", u"reset", None))

    def reset(self):
        self.paperTypeNameInput.clear()
        self.paperTypeDescInput.clear()

    def add(self):
        paperTypeName = self.paperTypeNameInput.text()
        paperTypeDesc = self.paperTypeDescInput.toPlainText()
        if paperTypeName == "":
            QMessageBox.warning(
                self, "warning", "paper type name can not be empty")
            return

        paperType = PaperType(paperTypeName, paperTypeDesc)

        if paperTypeDao.add(paperType):
            QMessageBox.information(self, "info", "add paper type success")
            self.reset()
        else:
            QMessageBox.information(
                self, "warning", "failed to add paper type, please try again")


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)

    main = Ui_MainWindow()
    main.show()

    sys.exit(app.exec())
